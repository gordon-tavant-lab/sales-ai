#!/usr/bin/env bash
# Package every shipped skill as a SELF-CONTAINED zip for claude.ai Desktop/web upload.
#
# spec 007 FR-015 / User Story 4 / SC-006. Zip structure follows Anthropic's documented
# requirement (support.claude.com/en/articles/12512198, "How to create custom skills",
# verified 2026-07-05): the skill's own folder must be the top-level entry inside the zip
# (SKILL.md nested one level in, at <skill-name>/SKILL.md) — NOT loose files at the zip root.
# claude.ai only reads a skill's `name` + `description` frontmatter fields on upload; any
# `allowed-tools`/hooks a vendored skill carries are inert on this surface (informational only).
#
# Self-containment (review finding F1, 2026-07-05): skills referencing shared content via
# ${CLAUDE_PLUGIN_ROOT}/playbooks|accelerators|assets get that content COPIED INTO the staged
# zip and the references rewritten to skill-local paths — a zip upload has no plugin root, so
# the repo-level sharing that works for the marketplace install would silently break here.
# The repo itself is never modified; rewriting happens in a temp staging dir only.
#
# Usage:
#   scripts/build-zips.sh                                        # build all shipped skills
#   scripts/build-zips.sh tvt-intel-customer tvt-create-pptx     # only the named skills
#
# Output: dist/<skill-name>.zip. dist/ is gitignored — build artifacts, regenerate any time.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$REPO_ROOT/dist"
SKILLS_DIR="$REPO_ROOT/skills"

cd "$REPO_ROOT"
mkdir -p "$DIST_DIR"

if [ "$#" -gt 0 ]; then
  SKILLS=("$@")
else
  SKILLS=()
  for d in "$SKILLS_DIR"/*/; do
    d="$(basename "$d")"
    [ -f "$SKILLS_DIR/$d/SKILL.md" ] && SKILLS+=("$d")
  done
fi

if [ "${#SKILLS[@]}" -eq 0 ]; then
  echo "error: no skill directories with a SKILL.md found under skills/ (run from the repo root)" >&2
  exit 1
fi

echo "Building ${#SKILLS[@]} skill zip(s) into $DIST_DIR ..."
built=0
failed=()

for skill in "${SKILLS[@]}"; do
  src="$SKILLS_DIR/$skill"
  if [ ! -d "$src" ] || [ ! -f "$src/SKILL.md" ]; then
    echo "  SKIP  $skill (no SKILL.md under skills/)"
    failed+=("$skill")
    continue
  fi

  zip_path="$DIST_DIR/${skill}.zip"
  rm -f "$zip_path"

  stage="$(mktemp -d)"
  cp -R "$src" "$stage/$skill"

  # Self-containment pass: if the skill references shared plugin-root content, copy exactly
  # the referenced top-level dirs in and rewrite the references to skill-local paths.
  # Bundled content can itself reference OTHER shared dirs transitively (e.g. a rubric that
  # points at assets/tavant-template.pptx) — repeat the pass until it's a no-op (fixed point;
  # two passes covers every depth seen in practice, and a third confirms convergence).
  bundled=""
  for _pass in 1 2 3; do
    changed=0
    for shared in playbooks accelerators assets rubrics references; do
      if [ ! -d "$stage/$skill/$shared" ] && grep -rq "\${CLAUDE_PLUGIN_ROOT}/$shared/" "$stage/$skill" 2>/dev/null; then
        cp -R "$REPO_ROOT/$shared" "$stage/$skill/$shared"
        bundled="$bundled +$shared"
        changed=1
      fi
      if [ -d "$stage/$skill/$shared" ]; then
        grep -rl "\${CLAUDE_PLUGIN_ROOT}/$shared/" "$stage/$skill" 2>/dev/null | while read -r f; do
          perl -i -pe "s{\\\$\\{CLAUDE_PLUGIN_ROOT\\}/$shared/}{$shared/}g" "$f"
        done || true
      fi
    done
    if [ "$changed" -eq 0 ]; then break; fi
  done
  # Cross-skill dependency: a skill that invokes a SIBLING skill's scripts directly
  # (${CLAUDE_PLUGIN_ROOT}/skills/<other>/...) gets that sibling's directory copied in
  # under skills/<other>/, same rewrite pattern as the shared-content dirs above.
  for other in "$SKILLS_DIR"/*/; do
    other="$(basename "$other")"
    [ "$other" = "$skill" ] && continue
    if grep -rq "\${CLAUDE_PLUGIN_ROOT}/skills/$other/" "$stage/$skill" 2>/dev/null; then
      mkdir -p "$stage/$skill/skills"
      cp -R "$SKILLS_DIR/$other" "$stage/$skill/skills/$other"
      grep -rl "\${CLAUDE_PLUGIN_ROOT}/skills/$other/" "$stage/$skill" 2>/dev/null | while read -r f; do
        perl -i -pe "s{\\\$\\{CLAUDE_PLUGIN_ROOT\\}/skills/$other/}{skills/$other/}g" "$f"
      done
      bundled="$bundled +skills/$other"
    fi
  done
  # Any remaining plugin-root refs (e.g. sibling-PLUGIN discovery, not sibling-skill-in-this-
  # plugin) can't work in a zip — surface them rather than shipping silently broken instructions.
  leftover="$(grep -rl 'CLAUDE_PLUGIN_ROOT' "$stage/$skill" 2>/dev/null || true)"
  note=""
  if [ -n "$leftover" ]; then
    note=" [WARN: unresolved plugin-root refs — works fully only via the Claude Code marketplace install]"
  fi

  (cd "$stage" && zip -rX -q "$zip_path" "$skill" \
    -x "*.pyc" -x "*/__pycache__/*" -x "*/.pytest_cache/*" -x "*/.DS_Store")
  rm -rf "$stage"

  echo "  OK    $skill -> $(basename "$zip_path") ($(du -h "$zip_path" | cut -f1))${bundled:+ [bundled:${bundled} ]}$note"
  built=$((built + 1))
done

echo ""
echo "Built $built/${#SKILLS[@]} zip(s) in $DIST_DIR"
echo "Reminder: releases/ holds the committed download-and-upload snapshots —"
echo "  cp dist/*.zip releases/   # then commit, so repo-zip downloaders get current skills"

if [ "${#failed[@]}" -gt 0 ]; then
  echo "Skipped (no SKILL.md): ${failed[*]}" >&2
  exit 1
fi
