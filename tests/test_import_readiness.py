"""Import-readiness gate — can someone who isn't the author install this plugin
from gitlab.tavant.com and actually use it?

This is the deterministic half of the judge (the LLM half is rubrics/import-readiness.md).
Every check answers spec 007 User Story 1: "Give a Claude Code instance with only this
plugin installed (no Workspace context) to someone who isn't Gordon."

Ratchet mechanics
-----------------
Known-open findings live in tests/import-gate-baseline.yml, keyed by stable violation
ids (no line numbers). Default pytest run fails only on:
  * NEW violations (a regression since the baseline), or
  * STALE baseline entries (a violation that got fixed but wasn't removed — keep it honest).
The publish gate ignores the baseline entirely:
  IMPORT_GATE_STRICT=1 python3 -m pytest tests/test_import_readiness.py
(or scripts/judge-import.sh --strict). Publishing to the marketplace requires a clean
strict run AND an empty baseline.

Regenerate the baseline (loud, deliberate — never to hide a regression):
  python3 tests/test_import_readiness.py --write-baseline
"""

import io
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
UNSHIPPED_DIR = ROOT / "unshipped"
BASELINE_PATH = Path(__file__).parent / "import-gate-baseline.yml"

# Guard: the fresh-clone check (C10) re-runs pytest inside a `git archive` copy.
# Skip the gate itself in that inner run or it recurses forever.
INNER_RUN = os.environ.get("IMPORT_GATE_INNER") == "1"
STRICT = os.environ.get("IMPORT_GATE_STRICT") == "1"

# ---------------------------------------------------------------- shared state

def shipped_skills() -> List[str]:
    return sorted(
        d.name for d in SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


def unshipped_skills() -> List[str]:
    if not UNSHIPPED_DIR.exists():
        return []
    return sorted(d.name for d in UNSHIPPED_DIR.iterdir() if d.is_dir())


def frontmatter(skill_md: Path) -> Dict:
    """Parse the YAML frontmatter block of a SKILL.md. Raises on malformed fences."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("no frontmatter fence at byte 0")
    end = text.index("\n---", 4)
    return yaml.safe_load(text[4:end])


def shipped_surface_files() -> List[Path]:
    """Every file a fresh installer's Claude actually reads. Excludes maintainer
    surfaces (docs/, tests/, unshipped/, .git, dist/)."""
    files = [ROOT / "README.md", ROOT / "CAPABILITIES.md"]
    files += sorted((ROOT / ".claude-plugin").glob("*.json"))
    for top in ("skills", "playbooks", "accelerators", "intel", "agents", "rubrics", "references"):
        d = ROOT / top
        if d.exists():
            files += sorted(
                p for p in d.rglob("*")
                if p.is_file() and p.suffix in (".md", ".json", ".yml", ".yaml", ".py", ".sh")
                and ".pytest_cache" not in p.parts and "__pycache__" not in p.parts
            )
    return files


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# ------------------------------------------------------------------ the checks
#
# Each check_* function returns a list of stable violation ids:
#   "<file>::<detail>"  — no line numbers, so ids survive unrelated edits.

SKILL_NAME_TOKEN = re.compile(r"\b(?:g|tvt)-[a-z][a-z0-9]*(?:-[a-z0-9]+)*\b")

# Tokens that look like skill names but aren't invocations of a missing skill.
NOT_SKILL_NAMES = {
    "g-pm-grow-out",        # spec 006 output dir name
    "tvt-pm-grow-out",      # documented default output dir of tvt-pm-grow
    "g-os-userland",        # upstream plugin family name, only valid in history notes
    "tvt-sales-skills",     # the plugin/marketplace name itself
    "tvt-skills",           # family shorthand, not a skill
}

FILE_EXT_AFTER_TOKEN = re.compile(r"^\.(md|py|sh|ya?ml|json|pptx|pdf|html|zip|txt)\b")


def skill_name_tokens(text):
    """Skill-name-shaped tokens that read as invocations — path components and
    filenames (validated by C6/C7 instead) are skipped."""
    out = set()
    for m in SKILL_NAME_TOKEN.finditer(text):
        if m.start() > 0 and text[m.start() - 1] == "/":
            continue  # path component, e.g. accelerators/tvt-sdlc-skills-platform.md
        if FILE_EXT_AFTER_TOKEN.match(text[m.end():m.end() + 6]):
            continue  # a filename, not a skill invocation
        if text[m.end():m.end() + 2] == "-*":
            continue  # family glob like `tvt-intel-*`, not a single skill
        out.add(m.group(0))
    return out


def check_C1_manifests() -> List[str]:
    """plugin.json / marketplace.json parse, carry required fields, and agree."""
    v = []
    pj_path = ROOT / ".claude-plugin" / "plugin.json"
    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        pj = json.loads(pj_path.read_text())
    except Exception as e:
        return ["{}::unparseable ({})".format(rel(pj_path), e)]
    try:
        mp = json.loads(mp_path.read_text())
    except Exception as e:
        return ["{}::unparseable ({})".format(rel(mp_path), e)]

    for field in ("name", "version", "description"):
        if not pj.get(field):
            v.append("{}::missing field '{}'".format(rel(pj_path), field))
    for field in ("name", "owner", "plugins"):
        if not mp.get(field):
            v.append("{}::missing field '{}'".format(rel(mp_path), field))
    plugins = mp.get("plugins") or []
    if len(plugins) != 1:
        v.append("{}::expected exactly 1 plugin entry, found {}".format(rel(mp_path), len(plugins)))
    else:
        entry = plugins[0]
        if entry.get("name") != pj.get("name"):
            v.append("{}::plugin name '{}' != plugin.json name '{}'".format(
                rel(mp_path), entry.get("name"), pj.get("name")))
        if entry.get("source") != ".":
            v.append("{}::plugin source must be '.' for a repo-root plugin, got '{}'".format(
                rel(mp_path), entry.get("source")))
    return v


def check_C2_skill_structure() -> List[str]:
    """Every skills/ dir has a SKILL.md whose frontmatter parses, name == dirname,
    description present and picker-sized. This is what the loader + claude.ai
    Desktop (which reads ONLY name + description) depend on."""
    v = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        md = d / "SKILL.md"
        if not md.exists():
            v.append("skills/{}::no SKILL.md — loader ships an empty skill".format(d.name))
            continue
        try:
            fm = frontmatter(md)
        except Exception as e:
            v.append("{}::frontmatter unparseable ({})".format(rel(md), e))
            continue
        name = fm.get("name")
        desc = fm.get("description")
        if name != d.name:
            v.append("{}::frontmatter name '{}' != directory name".format(rel(md), name))
        if name and not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", str(name)):
            v.append("{}::name '{}' violates [a-z0-9-] / 64-char convention".format(rel(md), name))
        if not desc or len(str(desc).strip()) < 50:
            v.append("{}::description missing or under 50 chars — dead at the picker".format(rel(md)))
        elif len(str(desc)) > 1024:
            v.append("{}::description over 1024 chars ({}) — truncated on claude.ai upload".format(
                rel(md), len(str(desc))))
    return v


def check_C3_dangling_skill_refs() -> List[str]:
    """The audit's Finding 1, generalized: every skill-name-shaped token mentioned
    anywhere in a shipped SKILL.md (or its references/) must exist in THIS package.
    A fresh install has no Workspace g-* skills to fall back on — every dangling
    name is an instruction the installee cannot follow."""
    known = set(shipped_skills())
    v = []
    for skill in shipped_skills():
        for f in sorted((SKILLS_DIR / skill).rglob("*.md")):
            for tok in sorted(skill_name_tokens(f.read_text(encoding="utf-8"))):
                if tok not in known and tok not in NOT_SKILL_NAMES:
                    v.append("{}::references '{}' which does not ship in this package".format(
                        rel(f), tok))
    return v


def check_C4_persona_leak() -> List[str]:
    """Wave-1 acceptance criterion, widened to the full shipped surface: the word
    'Gordon' (or his personal paths/emails outside manifest author fields) must not
    appear in anything an installee reads. One id per file."""
    v = []
    for f in shipped_surface_files():
        if f.name in ("plugin.json", "marketplace.json"):
            continue  # owner/author fields legitimately carry the maintainer's name
        text = f.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\bGordon\b", text) or "gordon.chan" in text:
            v.append("{}::persona leak ('Gordon')".format(rel(f)))
    return v


# Skills bundled with every Claude Code install (or common first-party marketplace
# skills) — a reference to these under .claude/skills/ is a legitimate cross-package
# composition, not author-machine coupling, unlike a reference to the author's own
# personal files (eval-policy.yml, quality-standard.md, etc.).
BUNDLED_SKILL_NAMES = {
    "pptx", "pptx-screenshot", "docx", "algorithmic-art", "brand-guidelines",
    "canvas-design", "frontend-design", "web-artifacts-builder", "slack-gif-creator",
    "theme-factory", "grill-me", "find-skills", "internal-comms",
}


def check_C5_workspace_coupling() -> List[str]:
    """References that only resolve on the author's machine: absolute home paths,
    Workspace-relative org/ trees, personal-infra artifacts."""
    patterns = [
        (r"/Users/[a-z]", "absolute /Users path"),
        (r"~/Workspace", "author home Workspace path"),
        (r"\borg/(playbooks|ai\+data|accelerators|domain|pov|public)\b", "Workspace org/ path"),
        (r"~/\.claude/(?!skills/)", "author-machine ~/.claude state (policy/CLAUDE.md)"),
        (r"\bspecs/\d{3}-", "outer-Workspace specs/ path — not shipped"),
        (r"\.specify/", "author-machine .specify path"),
        (r"\bagents?/logs\b|\bagent\.db\b", "author-machine agent infra"),
        (r"\bDemoServer\b|agent-lab\.io", "author-only demo infrastructure"),
    ]
    shipped = set(shipped_skills())
    claude_skills_ref = re.compile(r"\.claude/skills/([a-zA-Z0-9_-]+)/")
    # rubrics/import-readiness.md is a maintainer/judge rubric ABOUT catching these exact
    # patterns (its hard-fail criteria literally describe DemoServer/agent.db/etc as examples
    # of what to flag in OTHER skills) — not shipped skill instruction, so it's exempt from
    # the check it defines. The 5 real Output-Gate rubrics carry no such content and are
    # still fully scanned.
    v = []
    for f in shipped_surface_files():
        if f.name == "import-readiness.md" and f.parent.name == "rubrics":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for pat, label in patterns:
            if re.search(pat, text):
                v.append("{}::{}".format(rel(f), label))
        for name in sorted(set(claude_skills_ref.findall(text))):
            if name not in BUNDLED_SKILL_NAMES and name not in shipped:
                v.append("{}::author-machine .claude/skills/{}/ path (not bundled, not in this package)".format(rel(f), name))
    return v


def check_C6_plugin_root_refs() -> List[str]:
    """Every ${CLAUDE_PLUGIN_ROOT}/<path> must resolve inside the repo — these are
    load-bearing at invoke time under a marketplace install."""
    ref = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./+-]+)")
    v = []
    for f in shipped_surface_files():
        text = f.read_text(encoding="utf-8", errors="replace")
        for raw in sorted(set(ref.findall(text))):
            path = raw.rstrip(".,;:")
            if "{" in path or "*" in path or "<" in path:
                continue  # templated example, not a literal path
            if not (ROOT / path).exists():
                v.append("{}::${{CLAUDE_PLUGIN_ROOT}}/{} does not exist".format(rel(f), path))
    return v


def check_C7_markdown_links() -> List[str]:
    """Relative markdown links inside shipped skills must resolve on disk."""
    link = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
    v = []
    for skill in shipped_skills():
        for f in sorted((SKILLS_DIR / skill).rglob("*.md")):
            for target in sorted(set(link.findall(f.read_text(encoding="utf-8")))):
                if re.match(r"[a-z]+://|mailto:", target):
                    continue
                if "{" in target or "<" in target or "*" in target:
                    continue
                t = target.replace("${CLAUDE_PLUGIN_ROOT}", str(ROOT))
                resolved = (f.parent / t) if not t.startswith("/") else Path(t)
                if not resolved.exists():
                    v.append("{}::broken relative link '{}'".format(rel(f), target))
    return v


def check_C8_unshipped_isolation() -> List[str]:
    """unshipped/ must be genuinely out of the product: not in skills/, and no
    shipped skill may route to an unshipped name."""
    v = []
    unshipped = set(unshipped_skills())
    overlap = unshipped & set(shipped_skills())
    for name in sorted(overlap):
        v.append("skills/{}::skill exists in BOTH skills/ and unshipped/".format(name))
    for skill in shipped_skills():
        for f in sorted((SKILLS_DIR / skill).rglob("*.md")):
            toks = skill_name_tokens(f.read_text(encoding="utf-8"))
            for tok in sorted(toks & unshipped):
                v.append("{}::routes to unshipped skill '{}'".format(rel(f), tok))
    return v


def check_C9_scripts_compile() -> List[str]:
    """Every shipped .py must byte-compile under the Python this package documents
    (3.9 floor — `X | None` unions and match statements are regressions)."""
    v = []
    with tempfile.TemporaryDirectory() as tmp:
        for f in sorted(SKILLS_DIR.rglob("*.py")) + sorted((ROOT / "scripts").glob("*.py")):
            if "__pycache__" in f.parts or ".pytest_cache" in f.parts:
                continue
            try:
                py_compile.compile(str(f), doraise=True, cfile=os.path.join(tmp, "gate.pyc"))
            except py_compile.PyCompileError as e:
                v.append("{}::does not compile ({})".format(rel(f), str(e).splitlines()[0]))
    return v


def check_C10_fresh_clone() -> List[str]:
    """The install-what-git-has test: `git archive HEAD` into a temp dir (exactly the
    file set a `git clone` delivers — no untracked crutches) and run the package's
    own unit suite from there.

    Runs scripts/run_all_tests.sh, not a single `pytest` collection pass: several skills
    ship a same-named module (score.py, common.py) with no package namespacing, so one
    pytest process collecting them together silently reuses whichever it imported first
    for every later `from score import ...` — see pytest.ini and run_all_tests.sh."""
    if INNER_RUN:
        return []
    v = []
    with tempfile.TemporaryDirectory() as tmp:
        tar = subprocess.run(
            ["git", "-C", str(ROOT), "archive", "HEAD"],
            capture_output=True, check=True,
        )
        subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
        env = dict(os.environ, IMPORT_GATE_INNER="1")
        r = subprocess.run(
            ["bash", "scripts/run_all_tests.sh"],
            cwd=tmp, env=env, capture_output=True, text=True,
        )
        if r.returncode != 0:
            tail = "\n".join((r.stdout + r.stderr).splitlines()[-15:])
            v.append("<git-archive>::unit suite fails on a clean clone:\n{}".format(tail))
    return v


def check_C11_zips() -> List[str]:
    """The claude.ai-Desktop channel: rebuild every zip and verify the documented
    structure (skill dir top-level, SKILL.md one level in), zero unresolved
    plugin-root refs, and the tavantize template actually bundled."""
    if INNER_RUN:
        return []
    v = []
    with tempfile.TemporaryDirectory() as tmp:
        # Stage a clean copy so dist/ writes never touch the working tree.
        tar = subprocess.run(["git", "-C", str(ROOT), "archive", "HEAD"],
                             capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
        r = subprocess.run(["bash", "scripts/build-zips.sh"], cwd=tmp,
                           capture_output=True, text=True)
        if r.returncode != 0:
            return ["scripts/build-zips.sh::exits {}:\n{}".format(
                r.returncode, "\n".join((r.stdout + r.stderr).splitlines()[-10:]))]
        for line in r.stdout.splitlines():
            if "[WARN:" in line:
                skill = line.split()[1]
                v.append("dist/{}.zip::unresolved CLAUDE_PLUGIN_ROOT refs survive in the zip".format(skill))
        dist = Path(tmp) / "dist"
        for skill in shipped_skills():
            zp = dist / (skill + ".zip")
            if not zp.exists():
                v.append("dist/{}.zip::not built".format(skill))
                continue
            with zipfile.ZipFile(zp) as z:
                names = z.namelist()
                if not any(n == "{}/SKILL.md".format(skill) for n in names):
                    v.append("dist/{}.zip::SKILL.md not at <skill>/SKILL.md — claude.ai upload rejects it".format(skill))
                if any(not n.startswith(skill + "/") for n in names):
                    v.append("dist/{}.zip::loose files at zip root".format(skill))
        tav = dist / "tvt-tavantize.zip"
        if tav.exists():
            with zipfile.ZipFile(tav) as z:
                if "tvt-tavantize/assets/tavant-template.pptx" not in z.namelist():
                    v.append("dist/tvt-tavantize.zip::branded template not bundled — the skill's whole job")
    return v


def check_C12_claimed_counts() -> List[str]:
    """Every '<N> tvt-* skills' claim on the storefront surface must equal the real
    catalog count — the audit flagged count drift as a trust breaker."""
    actual = len([s for s in shipped_skills() if s.startswith("tvt-")])
    claim = re.compile(r"\b(\d+)\s+tvt-\*?\s*skills?\b")
    v = []
    for f in [ROOT / "README.md", ROOT / "CAPABILITIES.md",
              ROOT / ".claude-plugin" / "plugin.json",
              ROOT / ".claude-plugin" / "marketplace.json"]:
        if not f.exists():
            continue
        for n in claim.findall(f.read_text(encoding="utf-8")):
            if int(n) != actual:
                v.append("{}::claims {} tvt-* skills, catalog has {}".format(rel(f), n, actual))
    return v


ALL_CHECKS = [
    check_C1_manifests,
    check_C2_skill_structure,
    check_C3_dangling_skill_refs,
    check_C4_persona_leak,
    check_C5_workspace_coupling,
    check_C6_plugin_root_refs,
    check_C7_markdown_links,
    check_C8_unshipped_isolation,
    check_C9_scripts_compile,
    check_C10_fresh_clone,
    check_C11_zips,
    check_C12_claimed_counts,
]


# ------------------------------------------------------------- ratchet plumbing

def load_baseline() -> Dict[str, List[str]]:
    if not BASELINE_PATH.exists():
        return {}
    data = yaml.safe_load(BASELINE_PATH.read_text(encoding="utf-8")) or {}
    return {k: list(vv or []) for k, vv in data.get("findings", {}).items()}


def check_id(fn) -> str:
    return fn.__name__.replace("check_", "").split("_")[0]


@pytest.mark.skipif(INNER_RUN, reason="inner fresh-clone run — gate skipped to avoid recursion")
@pytest.mark.parametrize("check", ALL_CHECKS, ids=[fn.__name__ for fn in ALL_CHECKS])
def test_import_gate(check):
    cid = check_id(check)
    violations = check()
    baseline = load_baseline().get(cid, [])
    if STRICT:
        assert not violations, (
            "PUBLISH GATE [{}] — {} violation(s) block marketplace publication:\n  ".format(
                cid, len(violations)) + "\n  ".join(violations))
        return
    new = [x for x in violations if x not in baseline]
    stale = [x for x in baseline if x not in violations]
    msg = []
    if new:
        msg.append("REGRESSION [{}] — {} violation(s) not in the baseline:\n  {}".format(
            cid, len(new), "\n  ".join(new)))
    if stale:
        msg.append("STALE BASELINE [{}] — fixed, now remove from tests/import-gate-baseline.yml:\n  {}".format(
            cid, "\n  ".join(stale)))
    assert not msg, "\n\n".join(msg)


# --------------------------------------------------------- baseline regenerator

def write_baseline():
    findings = {}
    total = 0
    for fn in ALL_CHECKS:
        cid = check_id(fn)
        v = fn()
        if v:
            findings[cid] = v
            total += len(v)
        print("  {}: {} finding(s)".format(cid, len(v)))
    doc = {
        "comment": (
            "Known-open import-readiness findings. Each entry is debt the remediation "
            "waves must burn down; publishing requires this file to hold zero findings "
            "AND a clean IMPORT_GATE_STRICT=1 run. Never regenerate to hide a regression."
        ),
        "findings": findings,
    }
    BASELINE_PATH.write_text(
        yaml.safe_dump(doc, sort_keys=True, width=120, allow_unicode=True),
        encoding="utf-8")
    print("wrote {} ({} findings)".format(BASELINE_PATH, total))


if __name__ == "__main__":
    if "--write-baseline" in sys.argv:
        write_baseline()
    else:
        print(__doc__)
        sys.exit(2)
