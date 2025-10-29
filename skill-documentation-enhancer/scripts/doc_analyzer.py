#!/usr/bin/env python3
"""
Documentation Analyzer for Claude Skills

Analyzes SKILL.md files for completeness, clarity, and quality.
Scores documentation and identifies gaps.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class SkillDocAnalyzer:
    """Analyzes and scores skill documentation quality."""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_md_path = self.skill_path / "SKILL.md"

        if not self.skill_md_path.exists():
            raise FileNotFoundError(f"SKILL.md not found at {self.skill_md_path}")

        with open(self.skill_md_path, 'r') as f:
            self.content = f.read()

        self.frontmatter = self._parse_frontmatter()
        self.sections = self._parse_sections()
        self.scripts = self._find_scripts()

    def _parse_frontmatter(self) -> Dict[str, str]:
        """Extract YAML frontmatter."""
        match = re.search(r'^---\n(.*?)\n---', self.content, re.DOTALL)
        if not match:
            return {}

        fm = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip()
        return fm

    def _parse_sections(self) -> Dict[str, str]:
        """Extract major sections from SKILL.md."""
        sections = {}
        current_section = None
        current_content = []

        for line in self.content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _find_scripts(self) -> List[Path]:
        """Find all Python scripts in the skill."""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return []

        return list(scripts_dir.glob("*.py"))

    def analyze(self) -> Dict[str, any]:
        """Perform complete documentation analysis."""
        return {
            'frontmatter_score': self._score_frontmatter(),
            'structure_score': self._score_structure(),
            'example_score': self._score_examples(),
            'clarity_score': self._score_clarity(),
            'overall_score': 0,  # Calculated below
            'gaps': self._identify_gaps(),
            'suggestions': self._generate_suggestions()
        }

    def _score_frontmatter(self) -> Tuple[int, int, List[str]]:
        """Score frontmatter quality (max 20 points)."""
        score = 0
        max_score = 20
        issues = []

        # Check for required fields
        if 'name' in self.frontmatter:
            score += 5
        else:
            issues.append("Missing 'name' field in frontmatter")

        if 'description' in self.frontmatter:
            desc = self.frontmatter['description']
            score += 5

            # Check description quality
            if len(desc) > 50:
                score += 5
            else:
                issues.append("Description too short (< 50 chars)")

            # Check for TODO placeholders
            if 'TODO' in desc:
                score -= 5
                issues.append("Description contains TODO placeholder")

            # Check for trigger terms (keywords that would activate skill)
            trigger_keywords = ['when', 'activated by', 'use for', 'trigger']
            if any(kw in desc.lower() for kw in trigger_keywords):
                score += 5
            else:
                issues.append("Description lacks clear trigger terms")
        else:
            issues.append("Missing 'description' field in frontmatter")

        return (score, max_score, issues)

    def _score_structure(self) -> Tuple[int, int, List[str]]:
        """Score overall structure (max 25 points)."""
        score = 0
        max_score = 25
        issues = []

        recommended_sections = [
            ('Purpose' or 'Overview', 5),
            ('Usage', 5),
            ('Bundled Resources', 5),
            ('Best Practices', 5),
            ('Troubleshooting', 5)
        ]

        for section_name, points in recommended_sections:
            if section_name in self.sections:
                score += points
            else:
                issues.append(f"Missing recommended section: {section_name}")

        return (score, max_score, issues)

    def _score_examples(self) -> Tuple[int, int, List[str]]:
        """Score example coverage (max 30 points)."""
        score = 0
        max_score = 30
        issues = []

        # Check for code blocks
        code_blocks = re.findall(r'```.*?```', self.content, re.DOTALL)
        num_code_blocks = len(code_blocks)

        if num_code_blocks == 0:
            issues.append("No code examples found")
        elif num_code_blocks == 1:
            score += 10
            issues.append("Only one code example (consider adding more use cases)")
        elif num_code_blocks == 2:
            score += 20
        else:
            score += 30

        # Check if examples cover scripts
        if self.scripts:
            scripts_documented = 0
            for script in self.scripts:
                if script.name in self.content:
                    scripts_documented += 1

            if scripts_documented == 0:
                issues.append("No examples for bundled scripts")
            elif scripts_documented < len(self.scripts):
                issues.append(f"Only {scripts_documented}/{len(self.scripts)} scripts have examples")

        return (score, max_score, issues)

    def _score_clarity(self) -> Tuple[int, int, List[str]]:
        """Score clarity and readability (max 25 points)."""
        score = 20  # Start high, deduct for issues
        max_score = 25
        issues = []

        # Check for TODO markers
        todo_count = self.content.lower().count('todo')
        if todo_count > 0:
            score -= min(10, todo_count * 2)
            issues.append(f"Found {todo_count} TODO markers (incomplete documentation)")

        # Check for vague language
        vague_terms = ['something', 'things', 'stuff', 'etc.']
        vague_count = sum(self.content.lower().count(term) for term in vague_terms)
        if vague_count > 3:
            score -= 5
            issues.append(f"Contains vague language ({vague_count} instances)")

        # Bonus for clear structure
        if 'When to Use' in self.sections or 'When to use' in self.content:
            score += 5
        else:
            issues.append("No 'When to Use' guidance")

        return (score, max_score, issues)

    def _identify_gaps(self) -> List[str]:
        """Identify missing or weak documentation areas."""
        gaps = []

        # Check for trigger phrase documentation
        if 'trigger' not in self.content.lower() and 'activated' not in self.content.lower():
            gaps.append("No clear activation triggers documented")

        # Check for troubleshooting
        if 'Troubleshooting' not in self.sections and 'troubleshoot' not in self.content.lower():
            gaps.append("No troubleshooting section")

        # Check for script documentation
        if self.scripts and 'scripts/' not in self.content:
            gaps.append("Scripts exist but aren't documented")

        # Check for references documentation
        refs_dir = self.skill_path / "references"
        if refs_dir.exists() and list(refs_dir.glob("*.md")):
            if 'references/' not in self.content:
                gaps.append("Reference files exist but aren't documented")

        return gaps

    def _generate_suggestions(self) -> List[str]:
        """Generate specific improvement suggestions."""
        suggestions = []

        # Frontmatter improvements
        if 'description' in self.frontmatter:
            desc = self.frontmatter['description']
            if len(desc) < 100:
                suggestions.append(
                    f"Expand description to ~100-150 chars (currently {len(desc)}). "
                    "Include specific trigger terms and use cases."
                )

        # Example improvements
        if len(re.findall(r'```.*?```', self.content, re.DOTALL)) < 2:
            suggestions.append(
                "Add more usage examples: basic use case, intermediate, and advanced scenarios"
            )

        # Structure improvements
        if 'Troubleshooting' not in self.sections:
            suggestions.append(
                "Add Troubleshooting section with common issues and solutions"
            )

        if 'Best Practices' not in self.sections:
            suggestions.append(
                "Add Best Practices section with DO/DON'T guidance"
            )

        # Script documentation
        if self.scripts:
            for script in self.scripts:
                if script.name not in self.content:
                    suggestions.append(
                        f"Document script '{script.name}' with usage examples"
                    )

        return suggestions

    def print_report(self):
        """Print formatted analysis report."""
        analysis = self.analyze()

        # Calculate overall score
        total_score = (
            analysis['frontmatter_score'][0] +
            analysis['structure_score'][0] +
            analysis['example_score'][0] +
            analysis['clarity_score'][0]
        )
        total_max = (
            analysis['frontmatter_score'][1] +
            analysis['structure_score'][1] +
            analysis['example_score'][1] +
            analysis['clarity_score'][1]
        )
        overall_pct = int((total_score / total_max) * 100)

        print("\n" + "="*60)
        print(f"SKILL DOCUMENTATION ANALYSIS: {self.skill_path.name}")
        print("="*60)

        print(f"\n📊 OVERALL SCORE: {total_score}/{total_max} ({overall_pct}%)")

        if overall_pct >= 80:
            print("   ✓ Excellent documentation quality")
        elif overall_pct >= 60:
            print("   ⚠ Good, but could be improved")
        else:
            print("   ✗ Needs significant improvement")

        print("\n📋 COMPONENT SCORES:")
        print(f"   Frontmatter:  {analysis['frontmatter_score'][0]}/{analysis['frontmatter_score'][1]}")
        print(f"   Structure:    {analysis['structure_score'][0]}/{analysis['structure_score'][1]}")
        print(f"   Examples:     {analysis['example_score'][0]}/{analysis['example_score'][1]}")
        print(f"   Clarity:      {analysis['clarity_score'][0]}/{analysis['clarity_score'][1]}")

        if analysis['gaps']:
            print("\n🔍 IDENTIFIED GAPS:")
            for gap in analysis['gaps']:
                print(f"   • {gap}")

        if analysis['suggestions']:
            print("\n💡 SUGGESTIONS:")
            for suggestion in analysis['suggestions']:
                print(f"   • {suggestion}")

        # Show issues by category
        all_issues = []
        for key in ['frontmatter_score', 'structure_score', 'example_score', 'clarity_score']:
            all_issues.extend(analysis[key][2])

        if all_issues:
            print("\n⚠ ISSUES FOUND:")
            for issue in all_issues:
                print(f"   • {issue}")

        print("\n" + "="*60)
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Claude Skill documentation quality"
    )
    parser.add_argument(
        'skill_path',
        help="Path to skill directory containing SKILL.md"
    )
    parser.add_argument(
        '--enhance',
        action='store_true',
        help="Generate enhanced documentation (not yet implemented)"
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help="Interactive enhancement mode (not yet implemented)"
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help="Batch process multiple skills (not yet implemented)"
    )

    args = parser.parse_args()

    try:
        analyzer = SkillDocAnalyzer(args.skill_path)
        analyzer.print_report()

        if args.enhance or args.interactive or args.batch:
            print("⚠ Enhancement features not yet implemented")
            print("   Currently only analysis mode is available")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
