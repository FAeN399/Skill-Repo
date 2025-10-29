#!/usr/bin/env python3
"""
CSS Analyzer for static design skill.

Analyzes CSS for optimization opportunities.
"""

import sys
import re
from pathlib import Path


def analyze_css(file_path):
    """Analyze CSS file and provide suggestions."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return False

    suggestions = []
    stats = {}

    # Calculate file size
    file_size = len(content)
    stats['file_size_bytes'] = file_size
    stats['file_size_kb'] = round(file_size / 1024, 2)

    # Count lines
    lines = content.split('\n')
    stats['total_lines'] = len(lines)

    # Count selectors (rough estimate)
    selector_pattern = r'[^{]+\{'
    selectors = re.findall(selector_pattern, content)
    stats['selector_count'] = len(selectors)

    # Check for CSS custom properties
    if '--' in content and ':root' in content:
        stats['uses_custom_properties'] = True
    else:
        suggestions.append("Consider using CSS custom properties for theme values")

    # Check for modern layout methods
    if 'display: grid' in content or 'display:grid' in content:
        stats['uses_grid'] = True
    else:
        suggestions.append("Consider using CSS Grid for layouts")

    if 'display: flex' in content or 'display:flex' in content:
        stats['uses_flexbox'] = True
    else:
        suggestions.append("Consider using Flexbox for layouts")

    # Check for fixed pixel widths (potential responsiveness issue)
    fixed_width_pattern = r'width:\s*\d+px'
    fixed_widths = re.findall(fixed_width_pattern, content)
    if len(fixed_widths) > 5:
        suggestions.append(f"Found {len(fixed_widths)} fixed pixel widths. Consider relative units (%, rem, em)")

    # Check for !important overuse
    important_count = content.count('!important')
    if important_count > 3:
        suggestions.append(f"Found {important_count} uses of !important. Consider improving specificity instead")

    # Check for vendor prefixes (might be outdated)
    vendor_prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
    found_prefixes = [p for p in vendor_prefixes if p in content]
    if found_prefixes:
        suggestions.append(f"Found vendor prefixes: {', '.join(found_prefixes)}. Consider using autoprefixer")

    # Check for float-based layouts (outdated)
    if 'float:' in content or 'clear:' in content:
        suggestions.append("Float-based layouts detected. Consider modern alternatives (Grid/Flexbox)")

    # Check for overly specific selectors
    long_selectors = [s for s in selectors if s.count(' ') > 4]
    if long_selectors:
        suggestions.append(f"Found {len(long_selectors)} overly specific selectors. Simplify for better maintainability")

    # Print results
    print(f"\n{'='*60}")
    print(f"CSS Analysis Report: {file_path}")
    print(f"{'='*60}\n")

    print("STATISTICS:")
    print(f"  File size: {stats['file_size_kb']} KB ({stats['file_size_bytes']} bytes)")
    print(f"  Total lines: {stats['total_lines']}")
    print(f"  Selector count: {stats['selector_count']}")
    print(f"  Uses CSS custom properties: {stats.get('uses_custom_properties', False)}")
    print(f"  Uses CSS Grid: {stats.get('uses_grid', False)}")
    print(f"  Uses Flexbox: {stats.get('uses_flexbox', False)}")
    print()

    if suggestions:
        print(f"SUGGESTIONS ({len(suggestions)}):")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        print()
    else:
        print("✓ No suggestions! CSS looks well-optimized.")

    # Overall assessment
    if stats['file_size_kb'] < 10:
        print("File size: GOOD (< 10 KB)")
    elif stats['file_size_kb'] < 50:
        print("File size: ACCEPTABLE (10-50 KB)")
    else:
        print("File size: LARGE (> 50 KB) - Consider optimization")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python css_analyzer.py <css_file>")
        print("\nExample:")
        print("  python css_analyzer.py styles.css")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_css(file_path)


if __name__ == "__main__":
    main()
