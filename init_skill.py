#!/usr/bin/env python3
"""
Initialize a new Claude Skill with proper structure.

Usage:
    python init_skill.py <skill-name> [--path <output-directory>]
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


SKILL_MD_TEMPLATE = """---
name: {skill_name}
description: TODO: Describe what this skill does and when to use it. Be specific and include key terms that would trigger this skill.
---

# {skill_title}

TODO: Write a brief overview of what this skill provides.

## Overview

TODO: Describe the skill's purpose and capabilities.

## Usage

TODO: Provide instructions for using this skill.

### Quick Start

TODO: Show the most common use case with an example.

### Advanced Features

TODO: Document additional capabilities if applicable.

## Bundled Resources

### Scripts

- `scripts/example.py` - TODO: Describe what this script does

### References

- `references/example.md` - TODO: Describe what reference material this provides

### Assets

- `assets/example/` - TODO: Describe what assets are included

## Best Practices

TODO: Include tips for getting the best results with this skill.

## Troubleshooting

TODO: Document common issues and solutions.
"""

EXAMPLE_SCRIPT = """#!/usr/bin/env python3
\"\"\"
Example script for {skill_name} skill.

TODO: Replace this with actual functionality.
\"\"\"

def main():
    print("Hello from {skill_name}!")
    # TODO: Implement actual functionality
    pass


if __name__ == "__main__":
    main()
"""

EXAMPLE_REFERENCE = """# Example Reference

TODO: Replace this with actual reference documentation.

This file is loaded into context only when Claude determines it's needed,
keeping the main SKILL.md lean.

## Section 1

TODO: Add reference content

## Section 2

TODO: Add more reference content
"""

EXAMPLE_ASSET_README = """# Assets Directory

This directory contains files that will be used in Claude's output,
not loaded into the context window.

Examples:
- Templates (HTML, PowerPoint, etc.)
- Images, icons, logos
- Boilerplate code
- Fonts
- Sample documents

TODO: Add your asset files here and remove this README.
"""

README_TEMPLATE = """# {skill_title}

{description}

## Structure

This skill includes:
- `SKILL.md` - Main skill instructions
- `scripts/` - Executable code for deterministic tasks
- `references/` - Documentation loaded as needed
- `assets/` - Files used in output

## Development

Edit SKILL.md and bundled resources as needed.
Test the skill with real examples.

## Packaging

Package this skill for distribution:
```bash
python ../scripts/package_skill.py .
```
"""


def validate_skill_name(name: str) -> bool:
    """Validate skill name follows conventions."""
    if not name:
        return False
    if not all(c.isalnum() or c in '-_' for c in name):
        return False
    if name.startswith('-') or name.startswith('_'):
        return False
    return True


def create_skill_structure(skill_name: str, base_path: Path) -> None:
    """Create the skill directory structure."""
    skill_path = base_path / skill_name
    
    if skill_path.exists():
        print(f"Error: Directory '{skill_path}' already exists!")
        sys.exit(1)
    
    # Create main directories
    skill_path.mkdir(parents=True)
    (skill_path / "scripts").mkdir()
    (skill_path / "references").mkdir()
    (skill_path / "assets").mkdir()
    
    # Create SKILL.md
    skill_title = skill_name.replace('-', ' ').replace('_', ' ').title()
    skill_md_content = SKILL_MD_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )
    (skill_path / "SKILL.md").write_text(skill_md_content)
    
    # Create example script
    example_script = EXAMPLE_SCRIPT.format(skill_name=skill_name)
    script_path = skill_path / "scripts" / "example.py"
    script_path.write_text(example_script)
    script_path.chmod(0o755)  # Make executable
    
    # Create example reference
    (skill_path / "references" / "example.md").write_text(EXAMPLE_REFERENCE)
    
    # Create example asset README
    (skill_path / "assets" / "README.md").write_text(EXAMPLE_ASSET_README)
    
    print(f"✓ Created skill structure at: {skill_path}")
    print(f"\nNext steps:")
    print(f"1. Edit {skill_path}/SKILL.md")
    print(f"2. Add scripts, references, and assets as needed")
    print(f"3. Delete example files you don't need")
    print(f"4. Test the skill with real examples")
    print(f"5. Package: python scripts/package_skill.py {skill_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Skill with proper structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init_skill.py my-awesome-skill
  python init_skill.py bigquery-analyzer --path ./skills
  python init_skill.py pdf-processor --path ~/my-skills
        """
    )
    parser.add_argument(
        "skill_name",
        help="Name of the skill (use kebab-case, e.g., 'my-skill')"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Output directory for the skill (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Validate skill name
    if not validate_skill_name(args.skill_name):
        print("Error: Invalid skill name!")
        print("Skill name must:")
        print("  - Use lowercase letters, numbers, hyphens, or underscores")
        print("  - Not start with a hyphen or underscore")
        print("  - Use kebab-case (e.g., 'my-skill')")
        sys.exit(1)
    
    # Create skill structure
    base_path = Path(args.path).resolve()
    if not base_path.exists():
        print(f"Creating output directory: {base_path}")
        base_path.mkdir(parents=True)
    
    create_skill_structure(args.skill_name, base_path)


if __name__ == "__main__":
    main()
