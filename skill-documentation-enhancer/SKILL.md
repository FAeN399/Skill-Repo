---
name: skill-documentation-enhancer
description: Analyzes and improves skill documentation quality. Generates usage examples, troubleshooting guides, and best practices sections. Activated by "enhance documentation" or when creating/improving skills.
---

# Skill Documentation Enhancer

Transforms minimal skill documentation into comprehensive, practical guides. Analyzes existing skills and generates missing sections: usage examples, troubleshooting, best practices, and clearer descriptions.

## Purpose

Most skills have bare-minimum documentation that makes them hard to use effectively. This skill:
- Generates realistic usage examples from scripts and structure
- Creates troubleshooting sections from common error patterns
- Produces best practices based on skill capabilities
- Enhances frontmatter descriptions with better trigger terms
- Identifies documentation gaps and suggests improvements

## When to Use

**Trigger phrases:**
- "enhance documentation for [skill-name]"
- "improve skill docs"
- "generate examples for this skill"
- "analyze skill documentation quality"

**Use when:**
- Creating a new skill that needs comprehensive docs
- Inheriting a skill with minimal documentation
- Preparing skills for team/public distribution
- Documentation feels incomplete or unclear

## Usage

### Analyze Existing Skill

```bash
python scripts/doc_analyzer.py path/to/skill-name
```

**Output:**
- Documentation completeness score (0-100)
- Missing sections identified
- Example coverage analysis
- Suggested improvements with specific recommendations

### Generate Enhanced Documentation

```bash
python scripts/doc_analyzer.py path/to/skill-name --enhance
```

**Creates:**
- `SKILL_ENHANCED.md` with generated sections
- `examples/` directory with usage examples
- `TROUBLESHOOTING.md` if scripts have error handling
- Improved frontmatter description

### Interactive Enhancement

```bash
python scripts/doc_analyzer.py path/to/skill-name --interactive
```

**Workflow:**
1. Shows documentation analysis
2. Asks which sections to generate
3. Previews changes before applying
4. Updates SKILL.md in place

## Enhancement Process

### Step 1: Structure Analysis

The analyzer examines:
- **Frontmatter**: Is description specific? Does it include trigger terms?
- **Overview**: Is purpose clear? Are capabilities listed?
- **Usage section**: Are there examples? Multiple use cases shown?
- **Scripts**: Are they documented? Do examples exist?
- **References**: Are they described? When should they be loaded?
- **Troubleshooting**: Does it exist? Covers common issues?

### Step 2: Gap Identification

Common gaps detected:
- No usage examples (most common)
- Generic descriptions ("does X" without specifics)
- Undocumented script parameters
- Missing troubleshooting section
- No best practices guidance
- Weak trigger terms in frontmatter

### Step 3: Content Generation

**For examples:**
- Analyzes script signatures to generate realistic calls
- Creates basic → intermediate → advanced example progression
- Shows expected outputs
- Demonstrates error handling

**For troubleshooting:**
- Extracts error messages from scripts
- Generates common issue → solution pairs
- Documents prerequisite failures
- Links to related documentation

**For best practices:**
- Derives from skill structure (when to use scripts vs. references)
- Suggests optimization patterns
- Documents token efficiency tips
- Warns about common misuses

### Step 4: Quality Scoring

Scores based on:
- Example coverage (0-30 points): Examples for each major capability
- Clarity (0-25 points): Specific descriptions, clear trigger terms
- Completeness (0-25 points): All recommended sections present
- Practicality (0-20 points): Troubleshooting, best practices exist

## Bundled Resources

### Scripts

**`scripts/doc_analyzer.py`** - Main documentation analysis and enhancement tool

Features:
- Parses SKILL.md and analyzes structure
- Scores documentation quality
- Generates missing sections
- Supports interactive and batch modes

Usage:
```bash
# Analyze only
python scripts/doc_analyzer.py path/to/skill

# Analyze and enhance
python scripts/doc_analyzer.py path/to/skill --enhance

# Interactive mode
python scripts/doc_analyzer.py path/to/skill --interactive

# Batch process multiple skills
python scripts/doc_analyzer.py --batch path/to/skills/*
```

**`scripts/example_generator.py`** - Generates realistic usage examples from scripts

Features:
- Introspects Python scripts to find entry points
- Creates example commands with realistic parameters
- Generates expected output documentation
- Handles multiple example complexity levels

Usage:
```bash
# Generate examples for a script
python scripts/example_generator.py path/to/skill/scripts/tool.py

# Generate for all scripts in skill
python scripts/example_generator.py path/to/skill --all-scripts

# Output as markdown
python scripts/example_generator.py path/to/skill --format markdown
```

### References

**`references/documentation_patterns.md`** - Proven documentation structures and patterns

Loaded when: Skill documentation needs major restructuring or template guidance

Contains:
- Template for comprehensive skill docs
- Example progressions (basic → advanced)
- Troubleshooting section patterns
- Frontmatter description formulas
- Trigger term strategies

### Assets

**`assets/templates/`** - Documentation section templates

- `example_template.md` - Structure for usage examples
- `troubleshooting_template.md` - Common issue documentation format
- `best_practices_template.md` - Best practices section structure

## Best Practices

### For Analyzers

**DO:**
- Run analysis before submitting skills for review
- Use `--interactive` mode when learning patterns
- Generate examples for all major capabilities
- Check completeness score aims for 80+

**DON'T:**
- Over-generate examples (quality over quantity)
- Replace human-written examples with generated ones if originals are good
- Skip troubleshooting sections (users need them most)

### For Generated Content

**Quality checks:**
- Examples should be realistic (test them if possible)
- Troubleshooting should cover real error cases
- Best practices should be specific to the skill
- Descriptions should include actual trigger terms

**Integration:**
- Review generated content before accepting
- Customize templates for your domain
- Update generated sections as skill evolves
- Keep token efficiency in mind (don't add fluff)

## Troubleshooting

### "No examples generated"

**Cause:** Scripts have no clear entry points or parameters

**Solution:**
- Ensure scripts have `if __name__ == "__main__"` blocks
- Add argument parsers with `--help` documentation
- Manually specify example commands in `examples/` directory

### "Documentation score still low after enhancement"

**Cause:** Structure issues or missing critical sections

**Solution:**
- Check that frontmatter is specific and includes trigger terms
- Ensure Overview clearly states purpose
- Add at least one example per major capability
- Include troubleshooting for common failure modes

### "Generated examples don't match actual usage"

**Cause:** Script introspection incomplete or incorrect assumptions

**Solution:**
- Review `example_generator.py` output
- Manually edit `SKILL_ENHANCED.md` examples
- Add type hints to scripts for better inference
- Use `--interactive` mode to preview before accepting

### "Enhancement changes too much"

**Cause:** Analyzer detected major gaps and filled them all

**Solution:**
- Use `--interactive` mode to select specific sections
- Review `SKILL_ENHANCED.md` before replacing original
- Keep backups of original SKILL.md
- Customize enhancement via `doc_analyzer.py` parameters

## Extension Points

### Custom Analysis Rules

Add skill-specific quality checks:

```python
# In doc_analyzer.py
def custom_rule_checker(skill_path):
    # Check for domain-specific requirements
    if domain == "database":
        check_for_schema_docs()
    elif domain == "api":
        check_for_endpoint_examples()
```

### Template Customization

Create domain-specific templates:

```bash
cp assets/templates/example_template.md assets/templates/api_skill_template.md
# Edit for API-specific patterns
```

### Batch Enhancement

Process entire skill libraries:

```bash
python scripts/doc_analyzer.py --batch ~/my-skills/* --enhance --score-threshold 60
```

Only enhances skills scoring below 60, preserves well-documented skills.
