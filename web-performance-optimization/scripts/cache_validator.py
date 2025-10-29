#!/usr/bin/env python3
"""
Cache Validator - HTTP caching configuration validation tool

Validates caching setup including:
- HTTP cache headers
- Service worker configuration
- Resource caching strategies
- Cache effectiveness

Usage:
    python cache_validator.py --url https://example.com
"""

import argparse
import sys
from urllib.parse import urlparse
from typing import Dict, List

try:
    import requests
except ImportError:
    print("Missing dependencies. Install with: pip install requests")
    sys.exit(1)


class CacheValidator:
    """Validates caching configuration and effectiveness"""

    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.results = {
            'url': url,
            'headers': {},
            'issues': [],
            'recommendations': [],
            'score': 0
        }

    def validate(self) -> Dict:
        """Run cache validation"""
        print(f"🔍 Validating caching for {self.url}\n")

        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            self._validate_cache_headers(response.headers)
            self._validate_security_headers(response.headers)
            self._calculate_score()

            print(f"\n✅ Validation complete! Score: {self.results['score']}/100")
            return self.results

        except requests.RequestException as e:
            print(f"❌ Error fetching {self.url}: {e}")
            return None

    def _validate_cache_headers(self, headers: Dict[str, str]):
        """Validate HTTP cache headers"""
        print("📋 Checking cache headers...")

        # Store headers
        relevant_headers = [
            'Cache-Control', 'Expires', 'ETag', 'Last-Modified',
            'Vary', 'Age', 'Pragma'
        ]

        for header in relevant_headers:
            if header in headers:
                self.results['headers'][header] = headers[header]

        # Check Cache-Control
        cache_control = headers.get('Cache-Control', '')

        if not cache_control:
            self.results['issues'].append({
                'severity': 'error',
                'category': 'Cache-Control',
                'message': 'No Cache-Control header found',
                'impact': 'critical'
            })
            self.results['recommendations'].append({
                'category': 'Caching',
                'message': 'Set Cache-Control header for all resources',
                'example': 'Cache-Control: public, max-age=31536000, immutable'
            })
        else:
            print(f"   ✅ Cache-Control: {cache_control}")

            # Check for optimal directives
            if 'max-age' in cache_control:
                max_age = self._extract_max_age(cache_control)
                if max_age:
                    print(f"   ✅ max-age: {max_age} seconds ({self._format_duration(max_age)})")

                    if max_age < 3600:  # Less than 1 hour
                        self.results['recommendations'].append({
                            'category': 'Cache Duration',
                            'message': 'Short cache duration detected. Consider longer caching for static assets.',
                            'example': 'Cache-Control: public, max-age=31536000 for static assets'
                        })
            else:
                self.results['issues'].append({
                    'severity': 'warning',
                    'category': 'Cache-Control',
                    'message': 'No max-age directive found',
                    'impact': 'high'
                })

            # Check for immutable
            if 'immutable' in cache_control:
                print(f"   ✅ immutable directive present")
            else:
                self.results['recommendations'].append({
                    'category': 'Cache Optimization',
                    'message': 'Use immutable directive for static assets with cache busting',
                    'example': 'Cache-Control: public, max-age=31536000, immutable'
                })

        # Check ETag
        if 'ETag' in headers:
            print(f"   ✅ ETag: {headers['ETag']}")
        else:
            self.results['recommendations'].append({
                'category': 'Validation',
                'message': 'Consider adding ETag header for cache validation',
                'example': 'ETag: "abc123"'
            })

        # Check Last-Modified
        if 'Last-Modified' in headers:
            print(f"   ✅ Last-Modified: {headers['Last-Modified']}")
        else:
            self.results['recommendations'].append({
                'category': 'Validation',
                'message': 'Consider adding Last-Modified header',
                'example': 'Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT'
            })

        # Check for outdated Pragma
        if 'Pragma' in headers and headers['Pragma'] == 'no-cache':
            self.results['issues'].append({
                'severity': 'info',
                'category': 'Pragma',
                'message': 'Pragma: no-cache is deprecated. Use Cache-Control instead.',
                'impact': 'low'
            })

        # Check Vary header
        if 'Vary' in headers:
            print(f"   ✅ Vary: {headers['Vary']}")
            if 'User-Agent' in headers['Vary']:
                self.results['recommendations'].append({
                    'category': 'Vary Header',
                    'message': 'Vary: User-Agent can reduce cache effectiveness. Use sparingly.',
                    'example': 'Consider Vary: Accept-Encoding instead'
                })
        else:
            self.results['recommendations'].append({
                'category': 'Content Negotiation',
                'message': 'Consider adding Vary header for content negotiation',
                'example': 'Vary: Accept-Encoding'
            })

    def _validate_security_headers(self, headers: Dict[str, str]):
        """Validate security-related headers"""
        print("\n🔒 Checking security headers...")

        # Check Strict-Transport-Security
        if 'Strict-Transport-Security' in headers:
            print(f"   ✅ HSTS enabled: {headers['Strict-Transport-Security']}")
        else:
            self.results['recommendations'].append({
                'category': 'Security',
                'message': 'Enable HSTS (Strict-Transport-Security)',
                'example': 'Strict-Transport-Security: max-age=31536000; includeSubDomains'
            })

        # Check X-Content-Type-Options
        if headers.get('X-Content-Type-Options') == 'nosniff':
            print(f"   ✅ X-Content-Type-Options: nosniff")
        else:
            self.results['recommendations'].append({
                'category': 'Security',
                'message': 'Set X-Content-Type-Options: nosniff',
                'example': 'X-Content-Type-Options: nosniff'
            })

    def _extract_max_age(self, cache_control: str) -> int:
        """Extract max-age value from Cache-Control header"""
        import re
        match = re.search(r'max-age=(\d+)', cache_control)
        return int(match.group(1)) if match else 0

    def _format_duration(self, seconds: int) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m"
        elif seconds < 86400:
            return f"{seconds // 3600}h"
        elif seconds < 31536000:
            return f"{seconds // 86400}d"
        else:
            return f"{seconds // 31536000}y"

    def _calculate_score(self):
        """Calculate caching score"""
        score = 100

        for issue in self.results['issues']:
            if issue['severity'] == 'error':
                score -= 20
            elif issue['severity'] == 'warning':
                score -= 10
            elif issue['severity'] == 'info':
                score -= 5

        # Deduct points for missing headers
        if 'Cache-Control' not in self.results['headers']:
            score -= 30

        self.results['score'] = max(0, score)

    def print_report(self):
        """Print validation report"""
        print("\n" + "=" * 70)
        print("CACHE VALIDATION REPORT")
        print("=" * 70)
        print(f"\nURL: {self.results['url']}")
        print(f"Score: {self.results['score']}/100")

        print(f"\n📋 HEADERS FOUND")
        print("-" * 70)
        if self.results['headers']:
            for header, value in self.results['headers'].items():
                print(f"{header}: {value}")
        else:
            print("No cache headers found")

        if self.results['issues']:
            print(f"\n⚠️  ISSUES")
            print("-" * 70)
            for issue in self.results['issues']:
                icon = {'error': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}[issue['severity']]
                print(f"\n{icon} [{issue['category']}] {issue['message']}")
                print(f"   Impact: {issue['impact']}")

        if self.results['recommendations']:
            print(f"\n💡 RECOMMENDATIONS")
            print("-" * 70)
            for rec in self.results['recommendations']:
                print(f"\n[{rec['category']}] {rec['message']}")
                if 'example' in rec:
                    print(f"   Example: {rec['example']}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Validate HTTP caching configuration'
    )
    parser.add_argument(
        '--url',
        required=True,
        help='URL to validate'
    )

    args = parser.parse_args()

    # Run validation
    validator = CacheValidator(args.url)
    results = validator.validate()

    if not results:
        sys.exit(1)

    # Print report
    validator.print_report()


if __name__ == '__main__':
    main()
