# Eval Criteria Templates — Starter Rubrics

Pre-built rubrics for the 6 most common AI failure modes. Use directly with
`/tvt-core-eval score --criteria <template-path>`, or copy and customize.

| Template | Use For | Weight Profile |
|---|---|---|
| `hallucination.md` | Outputs that should be factually grounded | Heavily weighted on factual correctness |
| `instruction-following.md` | Outputs that must follow specific instructions | Heavy on instruction compliance |
| `refusal-appropriateness.md` | Anything where over-refusal or under-refusal is a risk | Two-sided — both wrongly-refused and wrongly-complied are failures |
| `schema-compliance.md` | Structured output (JSON, YAML, XML, specific markdown) | Binary on schema; secondary on content |
| `tool-call-correctness.md` | Agent outputs that invoke tools | Tool selection + argument validity + error handling |
| `prompt-injection-robustness.md` | Outputs from inputs that may be adversarial | Did the system resist injection attempts |

## How to use

**Inline reference:**
```
/tvt-core-eval score \
  --output draft.md \
  --criteria criteria/templates/hallucination.md   # path relative to this skill's own dir
```

**Compose multiple templates:**
```
/tvt-core-eval score \
  --output agent_output.md \
  --criteria templates/instruction-following.md \
  --eval-script "python3 check-with-template.py templates/tool-call-correctness.md"
```

**Customize:** Copy the template, edit the per-criterion weights, save under your
own project's `.claude-evals/criteria/`.

## Template structure

Every template follows this format so judges can score consistently:

```
# Criterion Name (weight: N)

**What to look for:** specific, observable behavior in the output.

**Score 1.0:** The output unambiguously demonstrates X.
**Score 0.5:** Partially demonstrates X / unclear.
**Score 0.0:** Fails to demonstrate X / contradicts X.

**Source:** citation for why this criterion matters.
```
