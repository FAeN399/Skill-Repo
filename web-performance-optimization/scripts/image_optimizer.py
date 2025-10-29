#!/usr/bin/env python3
"""
Image Optimizer - Batch image optimization and conversion tool

Optimizes images by:
- Converting to modern formats (WebP, AVIF)
- Generating responsive image sets
- Compressing with quality control
- Creating HTML picture elements

Usage:
    python image_optimizer.py --input ./images --output ./optimized
    python image_optimizer.py --input ./images --quality 85 --formats webp,avif
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple

try:
    from PIL import Image
    import pillow_avif  # For AVIF support
except ImportError:
    print("Missing dependencies. Install with: pip install Pillow pillow-avif-plugin")
    sys.exit(1)


class ImageOptimizer:
    """Optimizes and converts images for web performance"""

    SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'webp', 'avif']
    RESPONSIVE_SIZES = [400, 800, 1200, 1600, 2400]

    def __init__(self, quality=85, formats=None, responsive=True):
        self.quality = quality
        self.formats = formats or ['webp', 'avif']
        self.responsive = responsive
        self.stats = {
            'processed': 0,
            'skipped': 0,
            'original_size': 0,
            'optimized_size': 0
        }

    def optimize_directory(self, input_dir: Path, output_dir: Path):
        """Optimize all images in directory"""
        print(f"🖼️  Optimizing images from {input_dir} to {output_dir}")
        print(f"   Quality: {self.quality}")
        print(f"   Formats: {', '.join(self.formats)}")
        print(f"   Responsive: {self.responsive}\n")

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find all images
        image_files = []
        for ext in ['jpg', 'jpeg', 'png']:
            image_files.extend(input_dir.glob(f"**/*.{ext}"))
            image_files.extend(input_dir.glob(f"**/*.{ext.upper()}"))

        print(f"Found {len(image_files)} images to process\n")

        # Process each image
        for image_path in image_files:
            try:
                self._optimize_image(image_path, input_dir, output_dir)
            except Exception as e:
                print(f"❌ Error processing {image_path.name}: {e}")
                self.stats['skipped'] += 1

        # Print summary
        self._print_summary()

    def _optimize_image(self, image_path: Path, input_dir: Path, output_dir: Path):
        """Optimize a single image"""
        print(f"Processing: {image_path.name}")

        # Open image
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if needed (for JPEG)
            if img.mode == 'RGBA' and 'jpg' in self.formats:
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img

            # Get relative path for output structure
            rel_path = image_path.relative_to(input_dir)
            base_name = rel_path.stem
            sub_dir = rel_path.parent

            # Create subdirectory in output
            (output_dir / sub_dir).mkdir(parents=True, exist_ok=True)

            # Track original size
            original_size = image_path.stat().st_size
            self.stats['original_size'] += original_size

            # Generate responsive sizes
            if self.responsive:
                sizes = self._get_responsive_sizes(img.size[0])
                for size in sizes:
                    self._save_optimized(img, output_dir / sub_dir, base_name, size)
            else:
                self._save_optimized(img, output_dir / sub_dir, base_name)

            self.stats['processed'] += 1
            print(f"   ✅ Optimized ({original_size // 1024}KB)")

    def _get_responsive_sizes(self, original_width: int) -> List[int]:
        """Get appropriate responsive sizes for image"""
        return [size for size in self.RESPONSIVE_SIZES if size <= original_width * 1.2]

    def _save_optimized(self, img: Image, output_dir: Path, base_name: str, width: int = None):
        """Save optimized versions of image"""
        # Resize if width specified
        if width:
            aspect_ratio = img.size[1] / img.size[0]
            height = int(width * aspect_ratio)
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
            size_suffix = f"-{width}"
        else:
            resized_img = img
            size_suffix = ""
            width = img.size[0]

        # Save in each format
        for fmt in self.formats:
            if fmt in ['webp', 'avif']:
                output_path = output_dir / f"{base_name}{size_suffix}.{fmt}"
                resized_img.save(
                    output_path,
                    format=fmt.upper(),
                    quality=self.quality,
                    method=6 if fmt == 'webp' else 4
                )
                self.stats['optimized_size'] += output_path.stat().st_size

            elif fmt in ['jpg', 'jpeg']:
                output_path = output_dir / f"{base_name}{size_suffix}.jpg"
                resized_img.save(
                    output_path,
                    format='JPEG',
                    quality=self.quality,
                    optimize=True,
                    progressive=True
                )
                self.stats['optimized_size'] += output_path.stat().st_size

    def _print_summary(self):
        """Print optimization summary"""
        print("\n" + "=" * 60)
        print("OPTIMIZATION SUMMARY")
        print("=" * 60)
        print(f"Processed: {self.stats['processed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Original Size: {self.stats['original_size'] / 1024 / 1024:.2f} MB")
        print(f"Optimized Size: {self.stats['optimized_size'] / 1024 / 1024:.2f} MB")

        if self.stats['original_size'] > 0:
            savings = (1 - self.stats['optimized_size'] / self.stats['original_size']) * 100
            print(f"Savings: {savings:.1f}%")
        print("=" * 60)

    def generate_html_example(self, image_name: str, sizes: List[int]) -> str:
        """Generate example HTML picture element"""
        base_name = Path(image_name).stem

        html = f"""<!-- Optimized responsive image -->
<picture>
"""
        # AVIF sources
        if 'avif' in self.formats:
            html += f"""  <source
    type="image/avif"
    srcset="{', '.join([f'{base_name}-{s}.avif {s}w' for s in sizes])}">
"""

        # WebP sources
        if 'webp' in self.formats:
            html += f"""  <source
    type="image/webp"
    srcset="{', '.join([f'{base_name}-{s}.webp {s}w' for s in sizes])}">
"""

        # Fallback
        html += f"""  <img
    src="{base_name}-{sizes[1] if len(sizes) > 1 else sizes[0]}.jpg"
    srcset="{', '.join([f'{base_name}-{s}.jpg {s}w' for s in sizes])}"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 800px"
    alt="Description"
    loading="lazy"
    decoding="async">
</picture>
"""
        return html


def main():
    parser = argparse.ArgumentParser(
        description='Optimize images for web performance'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input directory containing images'
    )
    parser.add_argument(
        '--output',
        help='Output directory for optimized images (default: input_dir/optimized)'
    )
    parser.add_argument(
        '--quality',
        type=int,
        default=85,
        help='Image quality (0-100, default: 85)'
    )
    parser.add_argument(
        '--formats',
        default='webp,avif,jpg',
        help='Output formats (comma-separated, default: webp,avif,jpg)'
    )
    parser.add_argument(
        '--no-responsive',
        action='store_true',
        help='Disable responsive image generation'
    )
    parser.add_argument(
        '--example',
        action='store_true',
        help='Generate HTML example code'
    )

    args = parser.parse_args()

    # Parse paths
    input_dir = Path(args.input).resolve()
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        sys.exit(1)

    output_dir = Path(args.output or input_dir / 'optimized').resolve()

    # Parse formats
    formats = [fmt.strip() for fmt in args.formats.split(',')]

    # Create optimizer
    optimizer = ImageOptimizer(
        quality=args.quality,
        formats=formats,
        responsive=not args.no_responsive
    )

    # Run optimization
    optimizer.optimize_directory(input_dir, output_dir)

    # Generate example HTML
    if args.example:
        print("\n📝 Example HTML code:")
        print("-" * 60)
        example_html = optimizer.generate_html_example(
            'image',
            optimizer.RESPONSIVE_SIZES[:4]
        )
        print(example_html)


if __name__ == '__main__':
    main()
