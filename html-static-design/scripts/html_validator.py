#!/usr/bin/env python3
"""
HTML Validator for static design skill.

Validates HTML structure and checks for common issues.
"""

import sys
import re
from pathlib import Path


def validate_html(file_path):
    """Validate HTML file and report issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return False

    issues = []
    warnings = []

    # Check for DOCTYPE
    if not content.strip().startswith('<!DOCTYPE'):
        issues.append("Missing <!DOCTYPE html> declaration")

    # Check for viewport meta tag
    if '<meta name="viewport"' not in content:
        warnings.append("Missing viewport meta tag for responsive design")

    # Check for charset meta tag
    if '<meta charset=' not in content:
        warnings.append("Missing charset meta tag")

    # Check for semantic HTML5 elements
    semantic_elements = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
    found_semantic = any(f'<{elem}' in content for elem in semantic_elements)
    if not found_semantic:
        warnings.append("No semantic HTML5 elements found (header, nav, main, etc.)")

    # Check for images without alt attributes
    img_pattern = r'<img[^>]*>'
    images = re.findall(img_pattern, content)
    for img in images:
        if 'alt=' not in img:
            issues.append(f"Image without alt attribute: {img[:50]}...")

    # Check for proper heading hierarchy
    h1_count = content.count('<h1')
    if h1_count == 0:
        warnings.append("No <h1> heading found")
    elif h1_count > 1:
        warnings.append(f"Multiple <h1> headings found ({h1_count}). Should have only one.")

    # Check for inline styles
    if 'style=' in content:
        warnings.append("Inline styles found. Consider using external CSS.")

    # Check for missing closing tags (basic check)
    for tag in ['div', 'section', 'article', 'header', 'footer', 'nav', 'main']:
        open_count = content.count(f'<{tag}')
        close_count = content.count(f'</{tag}>')
        if open_count != close_count:
            issues.append(f"Mismatched {tag} tags: {open_count} opening, {close_count} closing")

    # Print results
    print(f"\n{'='*60}")
    print(f"HTML Validation Report: {file_path}")
    print(f"{'='*60}\n")

    if not issues and not warnings:
        print("✓ No issues found! HTML looks good.")
        return True

    if issues:
        print(f"ISSUES ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
        print()

    if issues:
        print("Status: FAILED - Please fix issues above")
        return False
    else:
        print("Status: PASSED (with warnings)")
        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python html_validator.py <html_file>")
        print("\nExample:")
        print("  python html_validator.py index.html")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_html(file_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
