# Claude Code Integration Guide

This guide explains how to use Skill Forge with Claude Code for agentic skill creation.

## Overview

Claude Code is a command-line tool that enables Claude to work autonomously on coding tasks. Skill Forge is designed to work seamlessly with Claude Code, allowing you to delegate skill creation tasks directly to Claude.

## Prerequisites

1. Install Claude Code: Follow instructions at https://docs.claude.com/en/docs/claude-code
2. Install Skill Forge: `pip install -e .`
3. Ensure you have access to Claude Code (requires API access)

## Basic Workflow

### 1. Creating Skills with Claude Code

You can prompt Claude Code to create skills using natural language:

```bash
claude-code "Create a skill for analyzing SQLite databases with schema documentation"
```

Claude will:
- Use `init_skill.py` to create the structure
- Generate appropriate scripts and references
- Write comprehensive SKILL.md documentation
- Validate the result
- Package it for distribution

### 2. Prompting Best Practices

**Be specific about requirements:**
```bash
claude-code "Create a BigQuery analysis skill that includes:
- Script to validate SQL queries
- Reference docs with our table schemas
- Examples of common queries
- Support for parameterized queries"
```

**Reference existing patterns:**
```bash
claude-code "Create a PDF manipulation skill similar to the docx skill pattern, 
including form filling, text extraction, and merging capabilities"
```

**Iterate on existing skills:**
```bash
claude-code "Improve the bigquery-analyzer skill by adding support for 
query cost estimation and adding a query optimization reference"
```

## Advanced Usage

### Custom Skill Templates

Create custom skill templates that Claude Code can use:

```bash
# Create a template
python scripts/init_skill.py my-template --path ./templates

# Customize the template structure
# Edit SKILL.md, add scripts, references, assets

# Use with Claude Code
claude-code "Create a skill based on the my-template template for analyzing web logs"
```

### Multi-Step Skill Creation

Claude Code can handle complex, multi-step skill creation:

```bash
claude-code "Create a comprehensive frontend-webapp skill that:
1. Includes React and Vue template assets
2. Has a script to scaffold new components
3. References our design system documentation
4. Includes linting and formatting configs
5. Test and validate the final skill"
```

### Skill Maintenance

Use Claude Code for ongoing maintenance:

```bash
# Update an existing skill
claude-code "Update the pdf-processor skill to support PDF/A format"

# Migrate to new standards
claude-code "Migrate all skills in ./my-skills to the latest Skill Forge standards"

# Optimize skills
claude-code "Analyze and optimize the bigquery skill for token efficiency"
```

## Integration Patterns

### Pattern 1: Skill-from-Examples

Provide examples and let Claude create the skill:

```bash
claude-code "I have these 3 use cases for a skill:
1. [paste example 1]
2. [paste example 2]  
3. [paste example 3]

Create a skill that handles all these cases efficiently"
```

### Pattern 2: Skill-from-Docs

Point Claude to documentation:

```bash
claude-code "Create a skill for the Stripe API. 
Reference the docs at https://stripe.com/docs/api
Focus on payment processing and webhook handling"
```

### Pattern 3: Skill-from-Script

Start with existing scripts:

```bash
claude-code "I have these Python scripts in ./scripts/
Create a proper skill around them with:
- Clean SKILL.md documentation
- Reference docs for the API
- Proper error handling
- Usage examples"
```

## Skill Forge Commands in Claude Code

Claude Code can use all Skill Forge commands:

```bash
# Initialize
claude-code "python scripts/init_skill.py my-new-skill"

# Validate
claude-code "python scripts/forge.py validate ./my-skill"

# Analyze
claude-code "python scripts/forge.py analyze ./my-skill"

# Package
claude-code "python scripts/package_skill.py ./my-skill"
```

## Best Practices

### 1. Clear Requirements

Be explicit about what the skill should do:
- What problem does it solve?
- What are the main use cases?
- What resources should be included?
- What level of complexity is needed?

### 2. Iterative Development

Start simple and iterate:
```bash
# Step 1: Basic structure
claude-code "Create a basic skill for X"

# Step 2: Add features
claude-code "Add Y functionality to the X skill"

# Step 3: Optimize
claude-code "Optimize the X skill for token efficiency"
```

### 3. Validation Loop

Always validate after creation:
```bash
claude-code "Create skill X, then validate it and fix any issues"
```

### 4. Use Templates

Leverage existing skills as templates:
```bash
claude-code "Create a skill for Y using the pattern from skill X"
```

## Common Workflows

### Workflow 1: From Scratch

```bash
# Single command creation
claude-code "Create a comprehensive skill for managing Docker containers 
with scripts for common operations, reference docs for Docker API, 
and examples of typical workflows"
```

### Workflow 2: From Repository

```bash
# Analyze and create skill from existing code
claude-code "Analyze the code in ./src and create a skill that helps 
developers work with this codebase. Include relevant patterns, 
common operations, and gotchas."
```

### Workflow 3: Team Skill Library

```bash
# Batch create skills for team
claude-code "Create skills for our team's common workflows:
1. Database migration skill
2. API testing skill  
3. Deployment checklist skill
Organize them in ./team-skills/"
```

## Troubleshooting

### Issue: Claude Code can't find scripts

**Solution:** Ensure Skill Forge is in the PATH:
```bash
export PATH="$PATH:$(pwd)/scripts"
```

### Issue: Validation fails

**Solution:** Ask Claude Code to fix it:
```bash
claude-code "Validate ./my-skill and fix any validation errors"
```

### Issue: Skill is too complex

**Solution:** Request optimization:
```bash
claude-code "Simplify the X skill - split content into references, 
reduce token usage, and improve progressive disclosure"
```

## Tips for Maximum Effectiveness

1. **Be conversational** - Claude Code understands natural language
2. **Reference examples** - Point to existing skills or patterns
3. **Iterate openly** - Ask Claude to improve its own work
4. **Validate often** - Build validation into your prompts
5. **Learn patterns** - Study how Claude creates skills and replicate good patterns

## Example: Complete Skill Creation Session

```bash
# Initial creation
claude-code "Create a skill for Kubernetes operations"

# Review and iterate
claude-code "Add more examples to the k8s skill and include a troubleshooting guide"

# Validate
claude-code "Validate the k8s skill"

# Optimize
claude-code "Analyze the k8s skill token usage and optimize if needed"

# Package
claude-code "Package the k8s skill for distribution"

# Success!
```

## Resources

- [Skill Forge README](../README.md)
- [Skill Creation Guide](./SKILL_CREATION_GUIDE.md)
- [Best Practices](./BEST_PRACTICES.md)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)

---

**Pro Tip:** Save your successful Claude Code prompts in a file for reuse! Create a `prompts/` directory in your Skill Forge installation and store templates there.
