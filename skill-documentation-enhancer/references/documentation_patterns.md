# Documentation Patterns for Claude Skills

Proven structures and patterns for creating high-quality skill documentation.

## Frontmatter Formula

```yaml
---
name: skill-name-kebab-case
description: [Action verb] + [what it does] + [when/why to use]. Activated by [trigger term]. Use for [specific use case].
---
```

**Examples:**

```yaml
# Good
description: Analyzes Python code for security vulnerabilities. Activated by "security scan" or "check for vulnerabilities". Use for pre-commit security reviews.

# Bad
description: A tool for code analysis
```

**Trigger term strategies:**
- Include exact phrases users would say: "when I say X", "activated by Y"
- List 2-3 trigger variations
- Be specific (not "use for coding" but "use for pre-commit security reviews")

## Document Structure Template

```markdown
---
name: skill-name
description: [Specific, trigger-rich description]
---

# Skill Name

[One-sentence summary of transformation: input → skill → output]

## Purpose

[Why this skill exists - what problem it solves]

This skill:
- [Capability 1]
- [Capability 2]
- [Capability 3]

## When to Use

**Trigger phrases:**
- "phrase 1"
- "phrase 2"
- "phrase 3"

**Use when:**
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

## Usage

### [Most Common Use Case]

```bash
[example command]
```

**Output:**
[What user should expect to see]

### [Secondary Use Case]

[Pattern repeats]

## [Additional sections as needed]

## Bundled Resources

### Scripts

**`scripts/main_script.py`** - [What it does]

Features:
- [Feature 1]
- [Feature 2]

Usage:
```bash
[examples]
```

### References

**`references/guide.md`** - [What knowledge it provides]

Loaded when: [Specific condition]

Contains:
- [Topic 1]
- [Topic 2]

## Best Practices

### For [User Role/Context]

**DO:**
- [Specific recommendation]
- [Specific recommendation]

**DON'T:**
- [Common mistake to avoid]
- [Common mistake to avoid]

## Troubleshooting

### "[Error message or symptom]"

**Cause:** [Why this happens]

**Solution:**
- [Step-by-step fix]
- [Alternative if first doesn't work]

[Repeat for 3-5 common issues]
```

## Example Progression Pattern

Always show examples in complexity order:

### 1. Minimal Example
```bash
# Simplest possible use
python script.py input.txt
```

### 2. Common Use Case
```bash
# What most users will do
python script.py input.txt --format json --output results/
```

### 3. Advanced Usage
```bash
# Power user features
python script.py input.txt --format json --output results/ --parallel 4 --verbose
```

## Troubleshooting Section Patterns

### Pattern 1: Error Message Match

```markdown
### "ImportError: No module named 'xyz'"

**Cause:** Required dependency not installed

**Solution:**
```bash
pip install xyz
```
```

### Pattern 2: Symptom-Based

```markdown
### Script runs but produces no output

**Cause:** Input file empty or wrong format

**Solution:**
- Check input file has content: `cat input.txt`
- Verify format matches expected (JSON, CSV, etc.)
- Run with `--verbose` flag to see processing details
```

### Pattern 3: Prerequisites

```markdown
### "Permission denied" errors

**Cause:** Script requires write access to output directory

**Solution:**
- Ensure output directory exists: `mkdir -p output/`
- Check permissions: `ls -la output/`
- Run with sudo if system directory: `sudo python script.py`
```

## Frontmatter Description Formulas

### Formula 1: Action + Context + Trigger
```
[Verb] + [what] + [context]. Activated by "[trigger]". Use for [specific scenario].
```

Example:
```
description: Extracts data from PDFs including tables and images. Activated by "parse PDF" or "extract from PDF". Use for document processing workflows.
```

### Formula 2: Transformation Statement
```
Transforms [input] into [output]. Triggered when [condition]. Best for [use case].
```

Example:
```
description: Transforms messy CSV files into validated, clean datasets. Triggered when working with data imports. Best for ETL pipelines.
```

### Formula 3: Problem → Solution
```
Solves [problem] by [method]. Use when [situation]. Activate with "[trigger phrase]".
```

Example:
```
description: Solves dependency conflicts by analyzing package graphs. Use when pip install fails. Activate with "resolve dependencies" or "fix conflicts".
```

## Best Practices Section Patterns

### Pattern 1: Role-Based

```markdown
## Best Practices

### For First-Time Users
**DO:**
- Start with `--help` to understand options
- Use `--dry-run` to preview changes

**DON'T:**
- Skip the examples section
- Run on production data without testing

### For Advanced Users
**DO:**
- Combine with other tools via pipes
- Use batch mode for multiple files

**DON'T:**
- Bypass validation flags
- Ignore deprecation warnings
```

### Pattern 2: Context-Based

```markdown
## Best Practices

### When Processing Large Files
- Use `--chunk-size` to control memory usage
- Enable `--progress` to monitor completion
- Consider `--parallel` for multi-core processing

### When Integrating with CI/CD
- Always use `--strict` mode
- Set explicit `--timeout` values
- Log output to file for debugging
```

## Script Documentation Template

For each script in `scripts/`:

```markdown
**`scripts/script_name.py`** - [One-line purpose]

Features:
- [What it can do 1]
- [What it can do 2]
- [What it can do 3]

Usage:
```bash
# Basic
python scripts/script_name.py [required_arg]

# With options
python scripts/script_name.py [required_arg] --option value

# Advanced
python scripts/script_name.py [required_arg] --flag1 --flag2 value
```

Parameters:
- `required_arg` - [what it is]
- `--option` - [what it controls] (default: [value])
- `--flag1` - [what it enables]
```

## Reference Documentation Template

For each file in `references/`:

```markdown
**`references/guide.md`** - [What knowledge domain it covers]

Loaded when: [Specific trigger - be precise]

Contains:
- [Topic 1] - [Why it matters]
- [Topic 2] - [Why it matters]
- [Topic 3] - [Why it matters]

Use this reference for: [Specific scenarios where this knowledge is needed]
```

## Common Documentation Gaps

### Gap: Vague Triggers
**Bad:** "Use this skill for analysis"
**Good:** "Activated by 'analyze logs' or 'parse server logs'. Use for debugging production issues."

### Gap: No Expected Output
**Bad:**
```bash
python script.py input.txt
```

**Good:**
```bash
python script.py input.txt

# Output:
# Processed 150 records
# Found 3 issues
# Results saved to output/results.json
```

### Gap: Missing "When NOT to Use"
Add a note about limitations:

```markdown
## When NOT to Use

This skill is **not suitable** for:
- Files larger than 1GB (use streaming-parser skill instead)
- Real-time processing (designed for batch workflows)
- Binary formats other than PDF (supports PDF only)
```

### Gap: No Progressive Disclosure Guidance

```markdown
### References

**`references/advanced_patterns.md`** - Deep-dive into optimization strategies

⚠ **Load this reference only when:** User asks about performance optimization or processing > 10K records. Contains detailed algorithmic explanations (high token cost).
```

## Token Efficiency Tips

1. **Remove redundancy**: Don't explain what's in the code if code is self-documenting
2. **Use references for deep content**: Main SKILL.md should be <5K words
3. **Condense examples**: Show pattern once, don't repeat variations unnecessarily
4. **Assume Claude knowledge**: Don't explain Python basics, standard libraries, or common patterns
5. **Bullet over prose**: Lists are more scannable and token-efficient

## Quality Checklist

Before finalizing documentation:

- [ ] Frontmatter description >80 characters, includes triggers
- [ ] "When to Use" section with specific scenarios
- [ ] At least 3 usage examples (basic → advanced)
- [ ] Each script has usage documentation
- [ ] Troubleshooting covers top 3-5 issues
- [ ] Best practices include DO/DON'T guidance
- [ ] No TODO placeholders remain
- [ ] No vague language ("stuff", "things", "etc.")
- [ ] Expected outputs shown for examples
- [ ] References explain when to load (token efficiency)
