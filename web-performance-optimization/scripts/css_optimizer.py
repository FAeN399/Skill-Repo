#!/usr/bin/env python3
"""
CSS Optimizer - CSS analysis and optimization tool

Analyzes CSS files to identify:
- Unused styles
- Optimization opportunities
- Critical CSS extraction candidates
- Performance issues

Usage:
    python css_optimizer.py --input styles.css
    python css_optimizer.py --input styles.css --html index.html --output optimized.css
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


class CSSOptimizer:
    """Analyzes and optimizes CSS for performance"""

    def __init__(self, css_path: Path, html_path: Path = None):
        self.css_path = css_path
        self.html_path = html_path
        self.css_content = ""
        self.html_content = ""
        self.analysis = {
            'file': str(css_path),
            'size': 0,
            'selectors': 0,
            'rules': 0,
            'unused': [],
            'issues': [],
            'recommendations': []
        }

    def analyze(self) -> Dict:
        """Run CSS analysis"""
        print(f"🎨 Analyzing CSS: {self.css_path.name}")

        # Read CSS
        with open(self.css_path, 'r', encoding='utf-8') as f:
            self.css_content = f.read()

        self.analysis['size'] = len(self.css_content)
        print(f"   Size: {self._format_size(self.analysis['size'])}")

        # Read HTML if provided
        if self.html_path:
            with open(self.html_path, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            print(f"   HTML: {self.html_path.name}")

        # Run analyses
        self._analyze_selectors()
        self._analyze_expensive_properties()
        self._find_unused_selectors()
        self._check_vendor_prefixes()
        self._generate_recommendations()

        return self.analysis

    def _analyze_selectors(self):
        """Analyze CSS selectors"""
        # Remove comments
        css_no_comments = re.sub(r'/\*.*?\*/', '', self.css_content, flags=re.DOTALL)

        # Find all selectors
        selector_pattern = r'([^{}]+)\s*{'
        selectors = re.findall(selector_pattern, css_no_comments)

        self.analysis['selectors'] = len(selectors)
        self.analysis['rules'] = len(re.findall(r'}', css_no_comments))

        print(f"   Selectors: {self.analysis['selectors']}")
        print(f"   Rules: {self.analysis['rules']}")

    def _analyze_expensive_properties(self):
        """Find expensive CSS properties"""
        expensive_props = {
            'box-shadow': 'medium',
            'filter': 'high',
            'transform': 'low',  # Actually performant
            'opacity': 'low',    # Actually performant
            'position: fixed': 'medium',
            'will-change': 'high',  # Overuse can be problematic
        }

        issues = []

        # Check for expensive properties
        if 'box-shadow' in self.css_content:
            count = len(re.findall(r'box-shadow:', self.css_content))
            issues.append({
                'type': 'expensive_property',
                'property': 'box-shadow',
                'count': count,
                'severity': 'info',
                'message': f'box-shadow used {count} times. Consider limiting usage for better performance.'
            })

        if 'filter' in self.css_content:
            count = len(re.findall(r'filter:', self.css_content))
            issues.append({
                'type': 'expensive_property',
                'property': 'filter',
                'count': count,
                'severity': 'warning',
                'message': f'filter used {count} times. Can be expensive, especially on large elements.'
            })

        # Check for will-change overuse
        will_change_matches = re.findall(r'will-change:\s*([^;]+)', self.css_content)
        if len(will_change_matches) > 5:
            issues.append({
                'type': 'will_change_overuse',
                'count': len(will_change_matches),
                'severity': 'warning',
                'message': f'will-change used {len(will_change_matches)} times. Overuse can harm performance.'
            })

        # Check for layout-triggering properties in animations
        layout_props = ['width', 'height', 'top', 'left', 'margin', 'padding']
        for prop in layout_props:
            animation_pattern = rf'@keyframes[^{{]*{{[^}}]*{prop}\s*:'
            if re.search(animation_pattern, self.css_content, re.DOTALL):
                issues.append({
                    'type': 'animation_layout',
                    'property': prop,
                    'severity': 'error',
                    'message': f'Animating {prop} triggers layout. Use transform/opacity instead.'
                })

        self.analysis['issues'] = issues

    def _find_unused_selectors(self):
        """Find potentially unused selectors (requires HTML)"""
        if not self.html_content:
            return

        # Remove comments from CSS
        css_no_comments = re.sub(r'/\*.*?\*/', '', self.css_content, flags=re.DOTALL)

        # Extract selectors
        selector_pattern = r'([^{}]+)\s*{'
        selectors = re.findall(selector_pattern, css_no_comments)

        unused = []
        for selector in selectors:
            # Clean up selector
            selector = selector.strip()

            # Skip @-rules
            if selector.startswith('@'):
                continue

            # Extract class/id names
            classes = re.findall(r'\.([a-zA-Z0-9_-]+)', selector)
            ids = re.findall(r'#([a-zA-Z0-9_-]+)', selector)
            tags = re.findall(r'^([a-z][a-z0-9]*)', selector)

            # Check if used in HTML
            found = False

            for class_name in classes:
                if f'class="{class_name}"' in self.html_content or \
                   f"class='{class_name}'" in self.html_content or \
                   f'class=".*{class_name}.*"' in self.html_content:
                    found = True
                    break

            for id_name in ids:
                if f'id="{id_name}"' in self.html_content or \
                   f"id='{id_name}'" in self.html_content:
                    found = True
                    break

            if not found and (classes or ids):
                unused.append(selector)

        self.analysis['unused'] = unused[:20]  # Limit to 20 examples

        if unused:
            print(f"   ⚠️  Found {len(unused)} potentially unused selectors")

    def _check_vendor_prefixes(self):
        """Check for outdated vendor prefixes"""
        outdated_prefixes = {
            '-webkit-border-radius': 'border-radius (supported in all modern browsers)',
            '-moz-border-radius': 'border-radius (no longer needed)',
            '-webkit-box-shadow': 'box-shadow (supported in all modern browsers)',
            '-moz-box-shadow': 'box-shadow (no longer needed)',
        }

        for prefix, recommendation in outdated_prefixes.items():
            if prefix in self.css_content:
                self.analysis['issues'].append({
                    'type': 'outdated_prefix',
                    'property': prefix,
                    'severity': 'info',
                    'message': f'Remove {prefix}, use {recommendation}'
                })

    def _generate_recommendations(self):
        """Generate optimization recommendations"""
        recommendations = []

        # Size-based recommendations
        size_kb = self.analysis['size'] / 1024
        if size_kb > 100:
            recommendations.append({
                'category': 'File Size',
                'severity': 'warning',
                'message': f'CSS file is {size_kb:.1f}KB. Consider splitting or minifying.',
                'impact': 'high'
            })

        # Selector complexity
        if self.analysis['selectors'] > 500:
            recommendations.append({
                'category': 'Selectors',
                'severity': 'info',
                'message': f'{self.analysis["selectors"]} selectors found. Consider modular CSS organization.',
                'impact': 'medium'
            })

        # Unused styles
        if len(self.analysis['unused']) > 0:
            recommendations.append({
                'category': 'Unused Styles',
                'severity': 'warning',
                'message': f'{len(self.analysis["unused"])} potentially unused selectors. Consider removing.',
                'impact': 'medium'
            })

        # Add issue-based recommendations
        for issue in self.analysis['issues']:
            if issue['severity'] in ['error', 'warning']:
                recommendations.append({
                    'category': issue['type'],
                    'severity': issue['severity'],
                    'message': issue['message'],
                    'impact': 'medium' if issue['severity'] == 'warning' else 'high'
                })

        self.analysis['recommendations'] = recommendations

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f}KB"
        else:
            return f"{size_bytes / 1024 / 1024:.1f}MB"

    def print_report(self):
        """Print analysis report"""
        print("\n" + "=" * 70)
        print("CSS ANALYSIS REPORT")
        print("=" * 70)
        print(f"\n📄 File: {self.analysis['file']}")
        print(f"   Size: {self._format_size(self.analysis['size'])}")
        print(f"   Selectors: {self.analysis['selectors']}")
        print(f"   Rules: {self.analysis['rules']}")

        if self.analysis['unused']:
            print(f"\n🗑️  POTENTIALLY UNUSED SELECTORS")
            print("-" * 70)
            for selector in self.analysis['unused'][:10]:
                print(f"   - {selector}")
            if len(self.analysis['unused']) > 10:
                print(f"   ... and {len(self.analysis['unused']) - 10} more")

        if self.analysis['issues']:
            print(f"\n⚠️  PERFORMANCE ISSUES")
            print("-" * 70)
            for issue in self.analysis['issues']:
                icon = {'error': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}[issue['severity']]
                print(f"\n{icon} {issue['message']}")

        if self.analysis['recommendations']:
            print(f"\n💡 RECOMMENDATIONS")
            print("-" * 70)
            for rec in self.analysis['recommendations']:
                icon = {'error': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}[rec['severity']]
                print(f"\n{icon} [{rec['category'].upper()}] {rec['message']}")
                print(f"   Impact: {rec['impact']}")
        else:
            print(f"\n✅ No major issues detected!")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze and optimize CSS files'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input CSS file path'
    )
    parser.add_argument(
        '--html',
        help='HTML file to check for unused selectors'
    )
    parser.add_argument(
        '--output',
        help='Output file path for optimized CSS'
    )

    args = parser.parse_args()

    # Check input file
    css_path = Path(args.input).resolve()
    if not css_path.exists():
        print(f"❌ CSS file not found: {css_path}")
        sys.exit(1)

    # Check HTML file
    html_path = None
    if args.html:
        html_path = Path(args.html).resolve()
        if not html_path.exists():
            print(f"❌ HTML file not found: {html_path}")
            sys.exit(1)

    # Analyze CSS
    optimizer = CSSOptimizer(css_path, html_path)
    results = optimizer.analyze()

    # Print report
    optimizer.print_report()


if __name__ == '__main__':
    main()
