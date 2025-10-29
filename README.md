# 🛠️ Skill Forge

**A comprehensive toolkit for creating, packaging, and managing Claude Skills**

Skill Forge is your workshop for crafting high-quality SKILL.md files and bundled resources that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## 🎯 What are Skills?

Skills are modular, self-contained packages that transform Claude from a general-purpose AI into a specialized agent equipped with domain-specific knowledge. Think of them as "onboarding guides" that provide:

- **Specialized workflows** - Multi-step procedures for specific domains
- **Tool integrations** - Instructions for working with specific file formats or APIs  
- **Domain expertise** - Company-specific knowledge, schemas, business logic
- **Bundled resources** - Scripts, references, and assets for complex tasks

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/          - Executable code
    ├── references/       - Documentation loaded as needed
    └── assets/           - Files used in output
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Claude Code (optional, for agentic workflow)

### Installation

```bash
git clone https://github.com/yourusername/skill-forge.git
cd skill-forge
pip install -e .
```

### Create Your First Skill

```bash
# Using the CLI
python scripts/init_skill.py my-awesome-skill

# Or with the interactive forge
python scripts/forge.py create
```

### Package Your Skill

```bash
python scripts/package_skill.py path/to/my-awesome-skill
```

## 📚 Core Principles

### 1. Concise is Key
The context window is a public good. Only include information Claude doesn't already know. Challenge every paragraph: "Does this justify its token cost?"

### 2. Set Appropriate Degrees of Freedom
- **High freedom** (text instructions): Multiple valid approaches
- **Medium freedom** (pseudocode): Preferred patterns with variation
- **Low freedom** (specific scripts): Fragile operations requiring precision

### 3. Progressive Disclosure
Skills use three-level loading:
1. **Metadata** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude

## 🛠️ Tools & Scripts

### `init_skill.py`
Initialize a new skill with proper structure:
```bash
python scripts/init_skill.py skill-name --path ./my-skills
```

### `package_skill.py`
Validate and package a skill for distribution:
```bash
python scripts/package_skill.py path/to/skill-folder [output-dir]
```

### `forge.py` ✨ (New!)
Interactive CLI for skill creation and management:
```bash
python scripts/forge.py --help
```

Commands:
- `create` - Interactive skill creation wizard
- `validate` - Validate skill structure and content
- `lint` - Check best practices and optimization
- `analyze` - Analyze token usage and efficiency
- `migrate` - Upgrade skills to latest standards

### `validate_skill.py`
Standalone validation of skill structure:
```bash
python scripts/validate_skill.py path/to/skill
```

## 📖 Documentation

- [Skill Creation Guide](docs/SKILL_CREATION_GUIDE.md) - Step-by-step process
- [Best Practices](docs/BEST_PRACTICES.md) - Proven patterns and tips
- [Design Patterns](docs/DESIGN_PATTERNS.md) - Workflow and output patterns
- [Examples Gallery](examples/) - Real-world skill examples
- [API Reference](docs/API_REFERENCE.md) - Tool and script documentation

## 🎨 Examples

### Basic Skill
```
hello-world/
├── SKILL.md
└── scripts/
    └── greet.py
```

### Complex Skill
```
bigquery-analyzer/
├── SKILL.md
├── scripts/
│   ├── query_builder.py
│   └── schema_validator.py
├── references/
│   ├── finance_schema.md
│   ├── sales_schema.md
│   └── product_schema.md
└── assets/
    └── query_templates/
```

See the [examples/](examples/) directory for complete skill implementations.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone and install dev dependencies
git clone https://github.com/yourusername/skill-forge.git
cd skill-forge
pip install -e ".[dev]"

# Run tests
pytest tests/

# Lint code
ruff check .
```

## 🌟 Integration with Claude Code

Skill Forge is designed to work seamlessly with Claude Code. Use it to:

1. **Generate skills agentic-ally**: Prompt Claude Code to create skills using Skill Forge
2. **Iterate rapidly**: Let Claude Code refine and test skills
3. **Maintain consistency**: Automated validation ensures quality

### Example Claude Code Workflow

```
# In your terminal
claude-code "Create a new skill for analyzing SQLite databases with schema documentation"
```

Claude Code will use Skill Forge to:
- Initialize the skill structure
- Generate appropriate scripts and references
- Validate the result
- Package it for distribution

## 📊 Skill Quality Metrics

Skill Forge includes analysis tools to measure:
- **Token efficiency** - Context window usage
- **Complexity score** - Degree of freedom appropriateness
- **Coverage** - Documentation completeness
- **Reusability** - Resource organization

```bash
python scripts/forge.py analyze path/to/skill
```

## 🗺️ Roadmap

- [ ] Web-based skill editor
- [ ] Skill marketplace integration
- [ ] Advanced testing framework
- [ ] Multi-language support for scripts
- [ ] Visual skill builder
- [ ] Skill versioning system
- [ ] Community skill registry

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built on the foundation of Anthropic's Claude Skills system, with inspiration from:
- The Claude community's skill-building experiences
- Modern dev tool design patterns
- Open source tool development best practices

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/skill-forge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/skill-forge/discussions)
- **Documentation**: [docs/](docs/)

---

**Made with ❤️ for the Claude community**
