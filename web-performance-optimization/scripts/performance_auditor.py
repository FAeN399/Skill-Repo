#!/usr/bin/env python3
"""
Performance Auditor - Comprehensive web performance analysis tool

This script audits a website's performance using multiple metrics and provides
detailed recommendations for optimization.

Usage:
    python performance_auditor.py --url https://example.com
    python performance_auditor.py --url https://example.com --output report.json
"""

import argparse
import json
import sys
from urllib.parse import urlparse
from typing import Dict, List, Any

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Install with: pip install requests beautifulsoup4")
    sys.exit(1)


class PerformanceAuditor:
    """Audits web performance and provides optimization recommendations"""

    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.results = {
            'url': url,
            'timestamp': None,
            'metrics': {},
            'resources': {},
            'recommendations': [],
            'score': 0
        }

    def audit(self) -> Dict[str, Any]:
        """Run complete performance audit"""
        print(f"🔍 Auditing {self.url}...")

        try:
            # Fetch page
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Run audits
            self._audit_html(soup)
            self._audit_resources(soup)
            self._audit_images(soup)
            self._audit_scripts(soup)
            self._audit_styles(soup)
            self._audit_fonts(soup)
            self._audit_caching(response.headers)
            self._calculate_score()

            print(f"✅ Audit complete! Score: {self.results['score']}/100")
            return self.results

        except requests.RequestException as e:
            print(f"❌ Error fetching {self.url}: {e}")
            return None

    def _audit_html(self, soup: BeautifulSoup):
        """Audit HTML structure"""
        metrics = {}

        # DOM size
        all_elements = soup.find_all()
        metrics['dom_elements'] = len(all_elements)

        # Nesting depth
        metrics['max_nesting_depth'] = self._get_max_depth(soup)

        # Meta tags
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        metrics['has_viewport'] = viewport is not None

        charset = soup.find('meta', attrs={'charset': True})
        metrics['has_charset'] = charset is not None

        self.results['metrics']['html'] = metrics

        # Recommendations
        if metrics['dom_elements'] > 1500:
            self.results['recommendations'].append({
                'category': 'HTML',
                'severity': 'warning',
                'message': f"Large DOM size ({metrics['dom_elements']} elements). Target < 1500.",
                'impact': 'high'
            })

        if metrics['max_nesting_depth'] > 32:
            self.results['recommendations'].append({
                'category': 'HTML',
                'severity': 'warning',
                'message': f"Deep nesting detected ({metrics['max_nesting_depth']} levels). Target < 32.",
                'impact': 'medium'
            })

    def _get_max_depth(self, element, current_depth=0):
        """Calculate maximum nesting depth"""
        if not element.children:
            return current_depth

        max_child_depth = current_depth
        for child in element.children:
            if hasattr(child, 'children'):
                child_depth = self._get_max_depth(child, current_depth + 1)
                max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth

    def _audit_resources(self, soup: BeautifulSoup):
        """Audit resource counts"""
        resources = {
            'images': len(soup.find_all('img')),
            'scripts': len(soup.find_all('script', src=True)),
            'stylesheets': len(soup.find_all('link', rel='stylesheet')),
            'fonts': len(soup.find_all('link', attrs={'as': 'font'})),
            'total_requests': 0
        }

        resources['total_requests'] = (
            resources['images'] +
            resources['scripts'] +
            resources['stylesheets'] +
            resources['fonts']
        )

        self.results['resources'] = resources

        # Recommendations
        if resources['total_requests'] > 50:
            self.results['recommendations'].append({
                'category': 'Resources',
                'severity': 'warning',
                'message': f"High request count ({resources['total_requests']}). Consider bundling.",
                'impact': 'high'
            })

    def _audit_images(self, soup: BeautifulSoup):
        """Audit image optimization"""
        images = soup.find_all('img')
        issues = []

        for img in images:
            # Check for lazy loading
            if img.get('loading') != 'lazy':
                issues.append('missing_lazy_loading')

            # Check for dimensions
            if not img.get('width') or not img.get('height'):
                issues.append('missing_dimensions')

            # Check for modern formats
            picture = img.find_parent('picture')
            if not picture:
                issues.append('no_modern_formats')

            # Check for alt text
            if not img.get('alt'):
                issues.append('missing_alt')

        if 'missing_lazy_loading' in issues:
            self.results['recommendations'].append({
                'category': 'Images',
                'severity': 'info',
                'message': 'Some images missing lazy loading attribute',
                'impact': 'medium'
            })

        if 'missing_dimensions' in issues:
            self.results['recommendations'].append({
                'category': 'Images',
                'severity': 'warning',
                'message': 'Images without dimensions can cause layout shift (CLS)',
                'impact': 'high'
            })

        if 'no_modern_formats' in issues:
            self.results['recommendations'].append({
                'category': 'Images',
                'severity': 'info',
                'message': 'Consider using <picture> with WebP/AVIF formats',
                'impact': 'medium'
            })

    def _audit_scripts(self, soup: BeautifulSoup):
        """Audit JavaScript loading"""
        scripts = soup.find_all('script', src=True)
        render_blocking = []
        optimized = []

        for script in scripts:
            has_async = script.get('async') is not None
            has_defer = script.get('defer') is not None
            is_module = script.get('type') == 'module'

            if not (has_async or has_defer or is_module):
                render_blocking.append(script.get('src'))
            else:
                optimized.append(script.get('src'))

        if render_blocking:
            self.results['recommendations'].append({
                'category': 'JavaScript',
                'severity': 'error',
                'message': f"{len(render_blocking)} render-blocking scripts found. Add async/defer.",
                'impact': 'critical',
                'details': render_blocking[:5]  # Show first 5
            })

    def _audit_styles(self, soup: BeautifulSoup):
        """Audit CSS loading"""
        stylesheets = soup.find_all('link', rel='stylesheet')
        render_blocking = []

        # Check for inline critical CSS
        inline_styles = soup.find_all('style')
        has_inline_css = len(inline_styles) > 0

        for link in stylesheets:
            media = link.get('media')
            onload = link.get('onload')

            # If no media query or onload handler, it's render-blocking
            if not media and not onload:
                render_blocking.append(link.get('href'))

        if render_blocking and not has_inline_css:
            self.results['recommendations'].append({
                'category': 'CSS',
                'severity': 'warning',
                'message': 'No inline critical CSS detected. Consider inlining above-fold styles.',
                'impact': 'high'
            })

        if len(render_blocking) > 2:
            self.results['recommendations'].append({
                'category': 'CSS',
                'severity': 'warning',
                'message': f"{len(render_blocking)} render-blocking stylesheets. Consider bundling.",
                'impact': 'medium'
            })

    def _audit_fonts(self, soup: BeautifulSoup):
        """Audit font loading"""
        font_links = soup.find_all('link', attrs={'as': 'font'})
        font_faces = soup.find_all('style')

        # Check for font preloading
        preloaded_fonts = [link for link in font_links if link.get('rel') == 'preload']

        # Check font-display in CSS (basic check)
        has_font_display = False
        for style in font_faces:
            if 'font-display' in style.string or '':
                has_font_display = True
                break

        if not preloaded_fonts and len(font_links) > 0:
            self.results['recommendations'].append({
                'category': 'Fonts',
                'severity': 'info',
                'message': 'Consider preloading critical fonts to improve LCP',
                'impact': 'medium'
            })

        if not has_font_display:
            self.results['recommendations'].append({
                'category': 'Fonts',
                'severity': 'info',
                'message': 'Use font-display: swap to prevent invisible text',
                'impact': 'medium'
            })

    def _audit_caching(self, headers: Dict[str, str]):
        """Audit caching headers"""
        cache_control = headers.get('Cache-Control', '')
        expires = headers.get('Expires', '')
        etag = headers.get('ETag', '')

        has_caching = bool(cache_control or expires)

        if not has_caching:
            self.results['recommendations'].append({
                'category': 'Caching',
                'severity': 'error',
                'message': 'No caching headers found. Set Cache-Control headers.',
                'impact': 'critical'
            })

    def _calculate_score(self):
        """Calculate overall performance score"""
        score = 100

        # Deduct points based on severity
        for rec in self.results['recommendations']:
            severity = rec['severity']
            if severity == 'error':
                score -= 15
            elif severity == 'warning':
                score -= 10
            elif severity == 'info':
                score -= 5

        self.results['score'] = max(0, score)


def main():
    parser = argparse.ArgumentParser(
        description='Audit web performance and get optimization recommendations'
    )
    parser.add_argument(
        '--url',
        required=True,
        help='URL to audit'
    )
    parser.add_argument(
        '--output',
        help='Output file path (JSON format)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'text'],
        default='text',
        help='Output format'
    )

    args = parser.parse_args()

    # Run audit
    auditor = PerformanceAuditor(args.url)
    results = auditor.audit()

    if not results:
        sys.exit(1)

    # Output results
    if args.format == 'json' or args.output:
        output = json.dumps(results, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"\n📄 Report saved to {args.output}")
        else:
            print(output)
    else:
        # Text format
        print("\n" + "=" * 60)
        print(f"PERFORMANCE AUDIT REPORT")
        print("=" * 60)
        print(f"\nURL: {results['url']}")
        print(f"Score: {results['score']}/100")

        print(f"\n📊 METRICS")
        print("-" * 60)
        print(f"DOM Elements: {results['metrics']['html']['dom_elements']}")
        print(f"Max Nesting: {results['metrics']['html']['max_nesting_depth']}")
        print(f"Total Requests: {results['resources']['total_requests']}")
        print(f"  - Images: {results['resources']['images']}")
        print(f"  - Scripts: {results['resources']['scripts']}")
        print(f"  - Stylesheets: {results['resources']['stylesheets']}")

        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 60)

        if not results['recommendations']:
            print("✅ No issues found!")
        else:
            for rec in sorted(
                results['recommendations'],
                key=lambda x: {'error': 0, 'warning': 1, 'info': 2}[x['severity']]
            ):
                icon = {'error': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}[rec['severity']]
                print(f"\n{icon} [{rec['category'].upper()}] {rec['message']}")
                print(f"   Impact: {rec['impact']}")
                if 'details' in rec:
                    print(f"   Details: {', '.join(rec['details'])}")


if __name__ == '__main__':
    main()
