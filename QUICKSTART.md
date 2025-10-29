# Quick Start Guide

Get started with Skill Forge in 5 minutes!

## Installation

```bash
git clone https://github.com/yourusername/skill-forge.git
cd skill-forge
pip install -e .
```

## Create Your First Skill

### Option 1: Interactive Mode (Recommended)

```bash
python scripts/forge.py create
```

Follow the prompts to create your skill interactively.

### Option 2: Command Line

```bash
python scripts/init_skill.py my-first-skill
```

## Edit Your Skill

Navigate to your skill directory and edit `SKILL.md`:

```bash
cd my-first-skill
# Edit SKILL.md with your favorite editor
```

### Update the Frontmatter

```yaml
---
name: my-first-skill
description: Your skill description here - be specific and include key terms
---
```

### Add Your Content

Replace the TODO sections with:
- Overview of what the skill does
- Usage instructions
- Examples
- Best practices

## Add Resources

### Add a Script

Create a Python script in `scripts/`:

```python
#!/usr/bin/env python3
"""My useful script."""

def main():
    print("Hello from my skill!")

if __name__ == "__main__":
    main()
```

Make it executable:
```bash
chmod +x scripts/my_script.py
```

### Add Reference Documentation

Create a markdown file in `references/`:

```markdown
# My Reference

Detailed information that Claude loads only when needed.

## Section 1
...
```

### Add Assets

Place templates, images, or other assets in `assets/`:

```
assets/
├── template.html
├── logo.png
└── styles.css
```

## Validate Your Skill

```bash
python scripts/forge.py validate ./my-first-skill
```

Fix any errors shown.

## Analyze Token Usage

```bash
python scripts/forge.py analyze ./my-first-skill
```

Optimize if needed (aim for <5000 tokens in SKILL.md).

## Package Your Skill

```bash
python scripts/package_skill.py ./my-first-skill
```

This creates `my-first-skill.skill` ready for distribution!

## Tips for Success

### Keep It Concise
- Only include information Claude doesn't already know
- Use progressive disclosure (references for details)
- Challenge every paragraph

### Use Imperative Voice
```markdown
❌ You should do X
✅ Do X
```

### Test with Real Examples
- Create the skill for actual use cases
- Test with Claude before finalizing
- Iterate based on real usage

### Leverage Scripts for Deterministic Tasks
- If you're rewriting the same code repeatedly, script it
- Use scripts for error-prone operations
- Keep scripts simple and well-documented

### Organize References by Domain
```
references/
├── api_endpoints.md
├── database_schema.md
└── common_patterns.md
```

## Next Steps

1. **Study Examples**: Check out `examples/hello-world` for a complete example
2. **Read Best Practices**: See `docs/BEST_PRACTICES.md` for detailed guidance
3. **Use with Claude Code**: See `docs/CLAUDE_CODE_INTEGRATION.md` for agentic workflows
4. **Share Your Skills**: Contribute to the community!

## Common Workflows

### Create and Package
```bash
python scripts/forge.py create
python scripts/forge.py validate ./my-skill
python scripts/package_skill.py ./my-skill
```

### Validate and Optimize
```bash
python scripts/forge.py validate ./my-skill
python scripts/forge.py lint ./my-skill
python scripts/forge.py analyze ./my-skill
```

### Migrate Old Skills
```bash
python scripts/forge.py migrate ./old-skill
python scripts/forge.py validate ./old-skill
```

## Getting Help

- **Issues**: Open a GitHub issue
- **Questions**: Check the docs/ directory
- **Examples**: Study examples/ directory
- **Community**: Join discussions

## Resources

- [Full README](../README.md)
- [Skill Creation Guide](./SKILL_CREATION_GUIDE.md)
- [Best Practices](./BEST_PRACTICES.md)
- [Claude Code Integration](./CLAUDE_CODE_INTEGRATION.md)
- [API Reference](./API_REFERENCE.md)

---

Happy skill forging! 🛠️
