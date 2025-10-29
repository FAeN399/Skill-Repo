#!/usr/bin/env python3
"""
Bundle Analyzer - JavaScript bundle analysis tool

Analyzes JavaScript bundles to identify:
- Large dependencies
- Duplicate code
- Tree-shaking opportunities
- Bundle composition

Usage:
    python bundle_analyzer.py --input dist/bundle.js
    python bundle_analyzer.py --input dist/bundle.js --format html --output report.html
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple


class BundleAnalyzer:
    """Analyzes JavaScript bundles for optimization opportunities"""

    def __init__(self, bundle_path: Path):
        self.bundle_path = bundle_path
        self.bundle_size = bundle_path.stat().st_size
        self.analysis = {
            'file': str(bundle_path),
            'size': self.bundle_size,
            'size_formatted': self._format_size(self.bundle_size),
            'modules': {},
            'dependencies': [],
            'duplicates': [],
            'recommendations': []
        }

    def analyze(self) -> Dict:
        """Run complete bundle analysis"""
        print(f"📦 Analyzing bundle: {self.bundle_path.name}")
        print(f"   Size: {self._format_size(self.bundle_size)}\n")

        with open(self.bundle_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self._analyze_imports(content)
        self._analyze_dependencies(content)
        self._analyze_size_composition(content)
        self._generate_recommendations()

        return self.analysis

    def _analyze_imports(self, content: str):
        """Analyze import statements"""
        # Match various import patterns
        patterns = [
            r'import\s+.*?\s+from\s+["\']([^"\']+)["\']',  # ES6 imports
            r'require\(["\']([^"\']+)["\']\)',  # CommonJS
            r'import\(["\']([^"\']+)["\']\)',  # Dynamic imports
        ]

        imports = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            imports.update(matches)

        # Categorize imports
        external = []
        internal = []

        for imp in imports:
            if imp.startswith('.'):
                internal.append(imp)
            else:
                external.append(imp)

        self.analysis['modules'] = {
            'total': len(imports),
            'external': len(external),
            'internal': len(internal),
            'external_list': sorted(external),
            'internal_list': sorted(internal)
        }

        print(f"📚 Modules found: {len(imports)}")
        print(f"   External: {len(external)}")
        print(f"   Internal: {len(internal)}")

    def _analyze_dependencies(self, content: str):
        """Analyze large dependencies"""
        # Common large libraries
        large_libs = {
            'lodash': 70000,
            'moment': 50000,
            'jquery': 85000,
            'react': 40000,
            'vue': 60000,
            'angular': 150000,
            'axios': 15000,
            'd3': 250000,
            'three': 500000,
            'chart.js': 200000
        }

        found_libs = []
        for lib, estimated_size in large_libs.items():
            if lib in content.lower():
                found_libs.append({
                    'name': lib,
                    'estimated_size': estimated_size,
                    'formatted_size': self._format_size(estimated_size)
                })

        self.analysis['dependencies'] = found_libs

        if found_libs:
            print(f"\n📊 Large dependencies detected:")
            for lib in found_libs:
                print(f"   - {lib['name']}: ~{lib['formatted_size']}")

    def _analyze_size_composition(self, content: str):
        """Analyze what takes up space"""
        stats = {
            'total_chars': len(content),
            'total_lines': content.count('\n'),
            'comments': 0,
            'whitespace': 0,
            'code': 0
        }

        # Count comments
        single_line_comments = len(re.findall(r'//.*?$', content, re.MULTILINE))
        multi_line_comments = len(re.findall(r'/\*.*?\*/', content, re.DOTALL))
        stats['comments'] = single_line_comments + multi_line_comments

        # Estimate whitespace
        whitespace_chars = sum(1 for c in content if c in ' \t\n\r')
        stats['whitespace'] = whitespace_chars

        # Code is the rest
        stats['code'] = stats['total_chars'] - stats['whitespace']

        self.analysis['composition'] = stats

    def _generate_recommendations(self):
        """Generate optimization recommendations"""
        recommendations = []

        # Size-based recommendations
        if self.bundle_size > 300 * 1024:  # 300KB
            recommendations.append({
                'severity': 'error',
                'category': 'Bundle Size',
                'message': f'Bundle size ({self._format_size(self.bundle_size)}) exceeds 300KB. Implement code splitting.',
                'impact': 'critical'
            })
        elif self.bundle_size > 200 * 1024:  # 200KB
            recommendations.append({
                'severity': 'warning',
                'category': 'Bundle Size',
                'message': f'Bundle size ({self._format_size(self.bundle_size)}) approaching 300KB limit. Consider optimization.',
                'impact': 'high'
            })

        # Dependency recommendations
        for dep in self.analysis['dependencies']:
            if dep['name'] == 'lodash':
                recommendations.append({
                    'severity': 'warning',
                    'category': 'Dependencies',
                    'message': 'Use lodash-es instead of lodash for better tree-shaking',
                    'impact': 'high',
                    'fix': "import { debounce } from 'lodash-es'"
                })
            elif dep['name'] == 'moment':
                recommendations.append({
                    'severity': 'info',
                    'category': 'Dependencies',
                    'message': 'Consider using date-fns or day.js instead of moment.js',
                    'impact': 'high',
                    'fix': "moment.js is large (~50KB). date-fns is modular and smaller."
                })

        # Module recommendations
        if self.analysis['modules']['total'] > 50:
            recommendations.append({
                'severity': 'info',
                'category': 'Modules',
                'message': f"{self.analysis['modules']['total']} modules detected. Consider code splitting by route/feature.",
                'impact': 'medium'
            })

        self.analysis['recommendations'] = recommendations

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}GB"

    def print_report(self):
        """Print analysis report to console"""
        print("\n" + "=" * 70)
        print("BUNDLE ANALYSIS REPORT")
        print("=" * 70)
        print(f"\n📦 Bundle: {self.analysis['file']}")
        print(f"   Size: {self.analysis['size_formatted']}")

        print(f"\n📚 MODULES")
        print("-" * 70)
        print(f"Total: {self.analysis['modules']['total']}")
        print(f"External: {self.analysis['modules']['external']}")
        print(f"Internal: {self.analysis['modules']['internal']}")

        if self.analysis['modules']['external_list']:
            print(f"\nExternal dependencies:")
            for dep in self.analysis['modules']['external_list'][:10]:
                print(f"  - {dep}")
            if len(self.analysis['modules']['external_list']) > 10:
                print(f"  ... and {len(self.analysis['modules']['external_list']) - 10} more")

        if self.analysis['dependencies']:
            print(f"\n📊 LARGE DEPENDENCIES")
            print("-" * 70)
            for dep in self.analysis['dependencies']:
                print(f"{dep['name']}: ~{dep['formatted_size']}")

        if self.analysis['recommendations']:
            print(f"\n💡 RECOMMENDATIONS")
            print("-" * 70)
            for rec in self.analysis['recommendations']:
                icon = {'error': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}[rec['severity']]
                print(f"\n{icon} [{rec['category'].upper()}] {rec['message']}")
                print(f"   Impact: {rec['impact']}")
                if 'fix' in rec:
                    print(f"   Fix: {rec['fix']}")
        else:
            print(f"\n✅ No major issues detected!")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze JavaScript bundles for optimization opportunities'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Path to JavaScript bundle file'
    )
    parser.add_argument(
        '--output',
        help='Output file path for report'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'text', 'html'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    # Check input file
    bundle_path = Path(args.input).resolve()
    if not bundle_path.exists():
        print(f"❌ Bundle file not found: {bundle_path}")
        sys.exit(1)

    # Analyze bundle
    analyzer = BundleAnalyzer(bundle_path)
    results = analyzer.analyze()

    # Output results
    if args.format == 'json':
        output = json.dumps(results, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"\n📄 Report saved to {args.output}")
        else:
            print(output)
    elif args.format == 'html':
        html_output = generate_html_report(results)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(html_output)
            print(f"\n📄 HTML report saved to {args.output}")
        else:
            print(html_output)
    else:
        analyzer.print_report()


def generate_html_report(results: Dict) -> str:
    """Generate HTML report"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bundle Analysis Report</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 40px auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .stat {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .recommendation {{ padding: 15px; margin: 10px 0; border-left: 4px solid #ffa500; background: #fff8e1; }}
        .error {{ border-color: #f44336; background: #ffebee; }}
        .warning {{ border-color: #ff9800; background: #fff3e0; }}
        .info {{ border-color: #2196f3; background: #e3f2fd; }}
        .dep {{ display: inline-block; margin: 5px; padding: 5px 10px; background: #e0e0e0; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>📦 Bundle Analysis Report</h1>
    <div class="stat">
        <h2>Bundle Info</h2>
        <p><strong>File:</strong> {results['file']}</p>
        <p><strong>Size:</strong> {results['size_formatted']}</p>
    </div>

    <div class="stat">
        <h2>📚 Modules</h2>
        <p><strong>Total:</strong> {results['modules']['total']}</p>
        <p><strong>External:</strong> {results['modules']['external']}</p>
        <p><strong>Internal:</strong> {results['modules']['internal']}</p>
    </div>

    {generate_deps_html(results.get('dependencies', []))}
    {generate_recommendations_html(results.get('recommendations', []))}
</body>
</html>
"""
    return html


def generate_deps_html(deps: List[Dict]) -> str:
    """Generate HTML for dependencies section"""
    if not deps:
        return ""

    html = "<div class='stat'><h2>📊 Large Dependencies</h2>"
    for dep in deps:
        html += f"<span class='dep'>{dep['name']}: {dep['formatted_size']}</span>"
    html += "</div>"
    return html


def generate_recommendations_html(recommendations: List[Dict]) -> str:
    """Generate HTML for recommendations section"""
    if not recommendations:
        return "<div class='stat'><h2>✅ No issues detected!</h2></div>"

    html = "<h2>💡 Recommendations</h2>"
    for rec in recommendations:
        html += f"""
        <div class='recommendation {rec['severity']}'>
            <h3>[{rec['category']}] {rec['message']}</h3>
            <p><strong>Impact:</strong> {rec['impact']}</p>
            {f"<p><strong>Fix:</strong> {rec['fix']}</p>" if 'fix' in rec else ''}
        </div>
        """
    return html


if __name__ == '__main__':
    main()
