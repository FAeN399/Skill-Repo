#!/usr/bin/env python3
"""
Validate and package a Claude Skill for distribution.

Usage:
    python package_skill.py <path/to/skill-folder> [output-directory]
"""

import argparse
import os
import re
import sys
import zipfile
from pathlib import Path
from typing import List, Tuple
import yaml


class ValidationError(Exception):
    """Custom exception for skill validation errors."""
    pass


class SkillValidator:
    """Validates Claude Skill structure and content."""
    
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self) -> bool:
        """Run all validation checks."""
        try:
            self._check_skill_md_exists()
            self._validate_frontmatter()
            self._validate_structure()
            self._check_file_references()
            self._check_token_budget()
            
            return len(self.errors) == 0
        except ValidationError as e:
            self.errors.append(str(e))
            return False
    
    def _check_skill_md_exists(self):
        """Ensure SKILL.md exists."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            raise ValidationError("SKILL.md not found")
    
    def _validate_frontmatter(self):
        """Validate YAML frontmatter."""
        skill_md = self.skill_path / "SKILL.md"
        content = skill_md.read_text()
        
        # Extract frontmatter
        if not content.startswith("---"):
            raise ValidationError("SKILL.md must start with YAML frontmatter (---)")
        
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValidationError("Invalid YAML frontmatter format")
        
        try:
            frontmatter = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            raise ValidationError(f"Invalid YAML frontmatter: {e}")
        
        # Check required fields
        if not isinstance(frontmatter, dict):
            raise ValidationError("Frontmatter must be a YAML dictionary")
        
        if "name" not in frontmatter:
            raise ValidationError("Frontmatter missing required 'name' field")
        
        if "description" not in frontmatter:
            raise ValidationError("Frontmatter missing required 'description' field")
        
        # Validate name
        name = frontmatter["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("'name' field must be a non-empty string")
        
        # Validate description
        description = frontmatter["description"]
        if not isinstance(description, str) or not description.strip():
            raise ValidationError("'description' field must be a non-empty string")
        
        # Check for TODOs in description
        if "TODO" in description or "TODO:" in description:
            self.warnings.append("Description contains TODO placeholders")
        
        # Check description length and quality
        if len(description) < 50:
            self.warnings.append(
                "Description is quite short. Consider adding more detail about "
                "what the skill does and when to use it."
            )
        
        # Check for extra fields (soft warning)
        extra_fields = set(frontmatter.keys()) - {"name", "description"}
        if extra_fields:
            self.warnings.append(
                f"Frontmatter contains extra fields: {', '.join(extra_fields)}. "
                "Only 'name' and 'description' are required."
            )
    
    def _validate_structure(self):
        """Validate directory structure."""
        # Check for README.md (should not exist)
        if (self.skill_path / "README.md").exists():
            self.warnings.append(
                "README.md found. Skills should only contain SKILL.md, not additional "
                "documentation files. Consider moving content to SKILL.md."
            )
        
        # Check for common extraneous files
        extraneous_files = [
            "INSTALLATION_GUIDE.md",
            "QUICK_REFERENCE.md", 
            "CHANGELOG.md",
            "CONTRIBUTING.md"
        ]
        
        for filename in extraneous_files:
            if (self.skill_path / filename).exists():
                self.errors.append(
                    f"{filename} found. Skills should not contain auxiliary "
                    "documentation files."
                )
    
    def _check_file_references(self):
        """Check that referenced files exist."""
        skill_md = self.skill_path / "SKILL.md"
        content = skill_md.read_text()
        
        # Find markdown links and references
        patterns = [
            r'\[([^\]]+)\]\(([^)]+)\)',  # [text](path)
            r'`([^`]+\.(py|sh|md|txt))`',  # `filename.ext`
        ]
        
        referenced_files = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    filepath = match[1] if len(match) > 1 else match[0]
                else:
                    filepath = match
                
                # Skip URLs
                if filepath.startswith(('http://', 'https://', '#')):
                    continue
                
                referenced_files.add(filepath)
        
        # Check if referenced files exist
        for filepath in referenced_files:
            full_path = self.skill_path / filepath
            if not full_path.exists():
                self.warnings.append(
                    f"Referenced file not found: {filepath}"
                )
    
    def _check_token_budget(self):
        """Check SKILL.md size."""
        skill_md = self.skill_path / "SKILL.md"
        content = skill_md.read_text()
        
        # Rough token estimate (1 token ≈ 4 characters)
        estimated_tokens = len(content) // 4
        
        if estimated_tokens > 5000:
            self.warnings.append(
                f"SKILL.md is large (~{estimated_tokens} tokens). "
                "Consider moving content to reference files."
            )
        
        # Check line count
        line_count = len(content.splitlines())
        if line_count > 500:
            self.warnings.append(
                f"SKILL.md has {line_count} lines. "
                "Consider keeping it under 500 lines and using references."
            )
    
    def print_results(self):
        """Print validation results."""
        if self.errors:
            print("\n❌ VALIDATION FAILED\n")
            print("Errors:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✓ VALIDATION PASSED")
        
        return len(self.errors) == 0


def package_skill(skill_path: Path, output_dir: Path) -> Path:
    """Package skill into a .skill file."""
    skill_name = skill_path.name
    output_file = output_dir / f"{skill_name}.skill"
    
    # Create zip file with .skill extension
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                # Skip hidden files, .pyc, and other build artifacts
                if file.startswith('.') or file.endswith(('.pyc', '.pyo')):
                    continue
                
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Validate and package a Claude Skill for distribution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python package_skill.py ./my-skill
  python package_skill.py ./skills/bigquery-analyzer ./dist
  python package_skill.py ~/my-skills/pdf-processor
        """
    )
    parser.add_argument(
        "skill_path",
        help="Path to skill directory"
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Output directory for .skill file (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    skill_path = Path(args.skill_path).resolve()
    if not skill_path.exists():
        print(f"Error: Skill directory not found: {skill_path}")
        sys.exit(1)
    
    if not skill_path.is_dir():
        print(f"Error: Not a directory: {skill_path}")
        sys.exit(1)
    
    output_dir = Path(args.output_dir).resolve() if args.output_dir else Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Validate skill
    print(f"Validating skill: {skill_path.name}")
    print(f"{'=' * 60}")
    
    validator = SkillValidator(skill_path)
    is_valid = validator.validate()
    validator.print_results()
    
    if not is_valid:
        print("\n❌ Packaging aborted due to validation errors.")
        print("Fix the errors above and try again.")
        sys.exit(1)
    
    # Package skill
    print(f"\n{'=' * 60}")
    print("Packaging skill...")
    
    try:
        output_file = package_skill(skill_path, output_dir)
        print(f"\n✓ Successfully packaged: {output_file}")
        print(f"  Size: {output_file.stat().st_size / 1024:.1f} KB")
    except Exception as e:
        print(f"\n❌ Packaging failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
