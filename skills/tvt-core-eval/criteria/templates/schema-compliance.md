# Schema Compliance Rubric

Use when the output must follow a specific structured format: JSON, YAML, XML,
specific markdown structure, CSV, or any defined schema.

## Criterion 1: Format validity (weight: 5)

**What to look for:** Output parses successfully as the declared format. JSON
parses, YAML parses, XML is well-formed, etc.

**Score 1.0:** Parses cleanly.
**Score 0.5:** Parses with one minor fix (e.g., trailing comma in JSON).
**Score 0.0:** Doesn't parse / requires non-trivial repair.

**Source:** OpenAI structured outputs eval; Anthropic JSON mode tests.

## Criterion 2: Schema conformance (weight: 5)

**What to look for:** All required fields present; field types correct; no
unexpected extra fields when schema is closed.

**Score 1.0:** Fully conforms to declared schema.
**Score 0.5:** Missing one optional field, or one type coercion needed.
**Score 0.0:** Required field missing, wrong type on critical field, or
unexpected fields when closed schema specified.

**Source:** JSON Schema validator standard; Pydantic / Zod-style validation.

## Criterion 3: Constraint compliance (weight: 4)

**What to look for:** Enums match allowed values, ranges respected (min/max),
string formats correct (URLs, emails, dates).

**Score 1.0:** All constraints satisfied.
**Score 0.5:** One constraint violated (e.g., enum value misspelled but recognizable).
**Score 0.0:** Multiple constraints violated.

**Source:** standard schema validation.

## Criterion 4: Content quality within structure (weight: 2)

**What to look for:** The structured fields contain meaningful, non-placeholder
content. Empty arrays where data was expected, "TODO" strings, "lorem ipsum"
all fail this.

**Score 1.0:** All fields populated meaningfully.
**Score 0.5:** One field has placeholder-like content but format is correct.
**Score 0.0:** Multiple fields are empty / placeholder-only.

**Source:** common gotcha in structured-output evals.

## Note

This rubric weights format heavily because schema-output failures are usually
binary in production (parser fails, downstream system fails). Use a separate
rubric for content quality within the structure.
