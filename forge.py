#!/usr/bin/env python3
"""
Skill Forge - Interactive CLI for Claude Skill creation and management.

This is the main command-line interface that provides:
- Interactive skill creation wizard
- Validation and linting
- Token analysis and optimization
- Migration tools
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import subprocess


class SkillForge:
    """Main CLI application for Skill Forge."""
    
    def __init__(self):
        self.scripts_dir = Path(__file__).parent
    
    def create_interactive(self):
        """Interactive skill creation wizard."""
        print("🛠️  Skill Forge - Interactive Skill Creator")
        print("=" * 60)
        print()
        
        # Gather information
        skill_name = input("Skill name (kebab-case, e.g., 'my-skill'): ").strip()
        if not skill_name:
            print("Error: Skill name is required!")
            sys.exit(1)
        
        print()
        description = input("Brief description (what does it do?): ").strip()
        
        print()
        print("What will this skill include?")
        has_scripts = input("  Scripts? (y/n): ").lower().startswith('y')
        has_references = input("  Reference docs? (y/n): ").lower().startswith('y')
        has_assets = input("  Assets/templates? (y/n): ").lower().startswith('y')
        
        print()
        output_path = input("Output directory [current directory]: ").strip() or "."
        
        # Confirm
        print()
        print("Summary:")
        print(f"  Name: {skill_name}")
        print(f"  Description: {description}")
        print(f"  Scripts: {'Yes' if has_scripts else 'No'}")
        print(f"  References: {'Yes' if has_references else 'No'}")
        print(f"  Assets: {'Yes' if has_assets else 'No'}")
        print(f"  Output: {output_path}")
        print()
        
        confirm = input("Create this skill? (y/n): ")
        if not confirm.lower().startswith('y'):
            print("Cancelled.")
            sys.exit(0)
        
        # Create skill using init_skill.py
        init_script = self.scripts_dir / "init_skill.py"
        result = subprocess.run(
            [sys.executable, str(init_script), skill_name, "--path", output_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error creating skill: {result.stderr}")
            sys.exit(1)
        
        print(result.stdout)
        
        # Update SKILL.md with provided description
        skill_path = Path(output_path) / skill_name / "SKILL.md"
        if description and skill_path.exists():
            content = skill_path.read_text()
            content = content.replace(
                "description: TODO: Describe what this skill does",
                f"description: {description}"
            )
            skill_path.write_text(content)
            print(f"✓ Updated description in SKILL.md")
        
        # Clean up unused directories
        skill_dir = Path(output_path) / skill_name
        if not has_scripts:
            scripts_dir = skill_dir / "scripts"
            if scripts_dir.exists():
                for f in scripts_dir.iterdir():
                    f.unlink()
                scripts_dir.rmdir()
                print(f"✓ Removed unused scripts directory")
        
        if not has_references:
            refs_dir = skill_dir / "references"
            if refs_dir.exists():
                for f in refs_dir.iterdir():
                    f.unlink()
                refs_dir.rmdir()
                print(f"✓ Removed unused references directory")
        
        if not has_assets:
            assets_dir = skill_dir / "assets"
            if assets_dir.exists():
                for f in assets_dir.iterdir():
                    f.unlink()
                assets_dir.rmdir()
                print(f"✓ Removed unused assets directory")
        
        print()
        print("✓ Skill created successfully!")
        print(f"  Edit: {skill_dir}/SKILL.md")
    
    def validate(self, skill_path: str):
        """Validate a skill."""
        package_script = self.scripts_dir / "package_skill.py"
        
        # Run validation without packaging by checking first
        print(f"Validating: {skill_path}")
        print("=" * 60)
        
        # We'll just import and use the validator directly
        sys.path.insert(0, str(self.scripts_dir))
        from package_skill import SkillValidator
        
        validator = SkillValidator(Path(skill_path))
        is_valid = validator.validate()
        validator.print_results()
        
        sys.exit(0 if is_valid else 1)
    
    def lint(self, skill_path: str):
        """Check skill against best practices."""
        print(f"Linting: {skill_path}")
        print("=" * 60)
        print()
        
        skill_path = Path(skill_path)
        skill_md = skill_path / "SKILL.md"
        
        if not skill_md.exists():
            print("❌ SKILL.md not found")
            sys.exit(1)
        
        content = skill_md.read_text()
        issues = []
        suggestions = []
        
        # Check for TODOs
        todo_count = content.count("TODO")
        if todo_count > 0:
            issues.append(f"Found {todo_count} TODO placeholder(s)")
        
        # Check for imperative voice
        non_imperative = []
        for line in content.split('\n'):
            line_lower = line.lower().strip()
            if line_lower.startswith(('you should', 'you can', 'you must', 'you will')):
                non_imperative.append(line[:60])
        
        if non_imperative:
            suggestions.append(
                f"Consider using imperative voice instead of 'you' language:\n"
                + "\n".join(f"    • {line}" for line in non_imperative[:3])
            )
        
        # Check for excessive formatting
        bold_count = content.count('**')
        if bold_count > 40:
            suggestions.append(
                f"Lots of bold formatting ({bold_count // 2} instances). "
                "Consider reducing for readability."
            )
        
        # Check file organization
        has_scripts = (skill_path / "scripts").exists()
        has_references = (skill_path / "references").exists()
        has_assets = (skill_path / "assets").exists()
        
        if has_scripts:
            scripts = list((skill_path / "scripts").iterdir())
            if not scripts:
                suggestions.append("scripts/ directory is empty - consider removing it")
        
        if has_references:
            refs = list((skill_path / "references").iterdir())
            if not refs:
                suggestions.append("references/ directory is empty - consider removing it")
        
        if has_assets:
            assets = list((skill_path / "assets").iterdir())
            if not assets or (len(assets) == 1 and assets[0].name == "README.md"):
                suggestions.append("assets/ directory is empty - consider removing it")
        
        # Print results
        if issues:
            print("❌ Issues:")
            for issue in issues:
                print(f"  • {issue}")
            print()
        
        if suggestions:
            print("💡 Suggestions:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
            print()
        
        if not issues and not suggestions:
            print("✓ No issues found!")
        
        sys.exit(0)
    
    def analyze(self, skill_path: str):
        """Analyze token usage and complexity."""
        print(f"Analyzing: {skill_path}")
        print("=" * 60)
        print()
        
        skill_path = Path(skill_path)
        skill_md = skill_path / "SKILL.md"
        
        if not skill_md.exists():
            print("❌ SKILL.md not found")
            sys.exit(1)
        
        content = skill_md.read_text()
        
        # Token estimation (rough: 1 token ≈ 4 characters)
        estimated_tokens = len(content) // 4
        
        # Line count
        line_count = len(content.split('\n'))
        
        # Word count
        word_count = len(content.split())
        
        # Check resources
        scripts_count = 0
        references_count = 0
        assets_count = 0
        
        if (skill_path / "scripts").exists():
            scripts_count = len(list((skill_path / "scripts").rglob("*.py")))
        
        if (skill_path / "references").exists():
            references_count = len(list((skill_path / "references").rglob("*.md")))
        
        if (skill_path / "assets").exists():
            assets_count = len(list((skill_path / "assets").rglob("*")))
            # Don't count directories
            assets_count = sum(1 for f in (skill_path / "assets").rglob("*") if f.is_file())
        
        # Complexity score (simple heuristic)
        complexity = "Low"
        if scripts_count > 3 or references_count > 5 or assets_count > 10:
            complexity = "High"
        elif scripts_count > 1 or references_count > 2 or assets_count > 3:
            complexity = "Medium"
        
        # Print report
        print("📊 Token Analysis:")
        print(f"  Estimated tokens: ~{estimated_tokens:,}")
        print(f"  Lines: {line_count:,}")
        print(f"  Words: {word_count:,}")
        print()
        
        print("📦 Resources:")
        print(f"  Scripts: {scripts_count}")
        print(f"  References: {references_count}")
        print(f"  Assets: {assets_count}")
        print()
        
        print("🎯 Metrics:")
        print(f"  Complexity: {complexity}")
        print(f"  Context efficiency: {'Good' if estimated_tokens < 4000 else 'Consider optimization'}")
        print()
        
        if estimated_tokens > 5000:
            print("⚠️  SKILL.md is large. Consider:")
            print("  • Moving detailed content to references/")
            print("  • Splitting into multiple reference files")
            print("  • Removing redundant explanations")
        
        sys.exit(0)
    
    def migrate(self, skill_path: str):
        """Migrate skill to latest standards."""
        print(f"Migrating: {skill_path}")
        print("=" * 60)
        print()
        
        skill_path = Path(skill_path)
        skill_md = skill_path / "SKILL.md"
        
        if not skill_md.exists():
            print("❌ SKILL.md not found")
            sys.exit(1)
        
        content = skill_md.read_text()
        original_content = content
        changes = []
        
        # Check for old frontmatter format
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                
                # Check for license field (should be removed in new format)
                if "license:" in frontmatter:
                    # Remove license line
                    lines = frontmatter.split('\n')
                    lines = [l for l in lines if not l.strip().startswith('license:')]
                    frontmatter = '\n'.join(lines)
                    content = "---" + frontmatter + "---" + parts[2]
                    changes.append("Removed 'license' field from frontmatter")
        
        # Save changes
        if content != original_content:
            # Backup original
            backup_path = skill_md.with_suffix('.md.backup')
            backup_path.write_text(original_content)
            
            # Write updated content
            skill_md.write_text(content)
            
            print("✓ Migration complete!")
            print(f"  Backup saved: {backup_path}")
            print()
            print("Changes made:")
            for change in changes:
                print(f"  • {change}")
        else:
            print("✓ No migration needed - skill is up to date!")
        
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="Skill Forge - Interactive CLI for Claude Skill management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  create      Interactive skill creation wizard
  validate    Validate skill structure and content
  lint        Check best practices and style
  analyze     Analyze token usage and complexity
  migrate     Upgrade skill to latest standards

Examples:
  python forge.py create
  python forge.py validate ./my-skill
  python forge.py lint ./my-skill
  python forge.py analyze ./my-skill
  python forge.py migrate ./my-skill
        """
    )
    
    parser.add_argument(
        "command",
        choices=["create", "validate", "lint", "analyze", "migrate"],
        help="Command to execute"
    )
    parser.add_argument(
        "skill_path",
        nargs="?",
        help="Path to skill directory (not needed for 'create')"
    )
    
    args = parser.parse_args()
    
    forge = SkillForge()
    
    if args.command == "create":
        forge.create_interactive()
    elif args.command == "validate":
        if not args.skill_path:
            print("Error: skill_path required for validate command")
            sys.exit(1)
        forge.validate(args.skill_path)
    elif args.command == "lint":
        if not args.skill_path:
            print("Error: skill_path required for lint command")
            sys.exit(1)
        forge.lint(args.skill_path)
    elif args.command == "analyze":
        if not args.skill_path:
            print("Error: skill_path required for analyze command")
            sys.exit(1)
        forge.analyze(args.skill_path)
    elif args.command == "migrate":
        if not args.skill_path:
            print("Error: skill_path required for migrate command")
            sys.exit(1)
        forge.migrate(args.skill_path)


if __name__ == "__main__":
    main()
