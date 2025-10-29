#!/usr/bin/env python3
"""
Image Growth Experiment - Shattering Doubts Edition
===================================================
This script generates progressively larger and more complex fractal images,
demonstrating exponential visual growth and mathematical beauty.

Features:
- Mandelbrot set fractal generation
- Progressive size growth (small → massive)
- Color gradients for stunning visuals
- Multiple growth stages
- Performance optimized with numpy
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import os
from datetime import datetime

class ImageGrowthEngine:
    """Engine for generating progressively growing fractal images."""

    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def mandelbrot(self, width, height, max_iter=100, zoom=1, center_x=-0.5, center_y=0):
        """
        Generate Mandelbrot set fractal.

        Args:
            width: Image width in pixels
            height: Image height in pixels
            max_iter: Maximum iterations for convergence
            zoom: Zoom level (higher = more zoomed in)
            center_x, center_y: Center coordinates

        Returns:
            numpy array of iteration counts
        """
        # Create coordinate arrays
        x_min, x_max = center_x - 2/zoom, center_x + 2/zoom
        y_min, y_max = center_y - 2/zoom, center_y + 2/zoom

        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)

        # Complex plane
        C = X + 1j*Y
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)

        # Iterate
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i

        return M

    def create_colorful_image(self, fractal_data, width, height, palette="fire"):
        """
        Convert fractal data to colorful image.

        Args:
            fractal_data: numpy array of iteration counts
            width, height: Image dimensions
            palette: Color palette ("fire", "ocean", "psychedelic", "matrix")

        Returns:
            PIL Image object
        """
        # Normalize data
        normalized = (fractal_data - fractal_data.min()) / (fractal_data.max() - fractal_data.min() + 1e-10)

        # Create color arrays
        img_array = np.zeros((height, width, 3), dtype=np.uint8)

        if palette == "fire":
            # Fire palette: black → red → orange → yellow → white
            img_array[:, :, 0] = (255 * np.minimum(normalized * 3, 1)).astype(np.uint8)  # Red
            img_array[:, :, 1] = (255 * np.maximum(0, np.minimum((normalized - 0.33) * 3, 1))).astype(np.uint8)  # Green
            img_array[:, :, 2] = (255 * np.maximum(0, (normalized - 0.66) * 3)).astype(np.uint8)  # Blue

        elif palette == "ocean":
            # Ocean palette: deep blue → cyan → white
            img_array[:, :, 0] = (255 * np.maximum(0, (normalized - 0.5) * 2)).astype(np.uint8)  # Red
            img_array[:, :, 1] = (255 * normalized).astype(np.uint8)  # Green
            img_array[:, :, 2] = (255 * np.minimum(1, normalized * 1.5)).astype(np.uint8)  # Blue

        elif palette == "psychedelic":
            # Psychedelic rainbow
            img_array[:, :, 0] = (255 * np.abs(np.sin(normalized * np.pi * 3))).astype(np.uint8)
            img_array[:, :, 1] = (255 * np.abs(np.sin((normalized + 0.33) * np.pi * 3))).astype(np.uint8)
            img_array[:, :, 2] = (255 * np.abs(np.sin((normalized + 0.66) * np.pi * 3))).astype(np.uint8)

        elif palette == "matrix":
            # Matrix-style green
            img_array[:, :, 0] = (50 * normalized).astype(np.uint8)
            img_array[:, :, 1] = (255 * normalized).astype(np.uint8)
            img_array[:, :, 2] = (50 * normalized).astype(np.uint8)

        return Image.fromarray(img_array)

    def add_metadata_overlay(self, img, stage, size, generation_time):
        """Add metadata overlay to image."""
        draw = ImageDraw.Draw(img)

        # Add text overlay
        text = f"Growth Stage {stage} | Size: {size}x{size}px | Time: {generation_time:.2f}s"

        # Draw background rectangle for text
        bbox = draw.textbbox((10, 10), text)
        draw.rectangle(bbox, fill=(0, 0, 0, 180))
        draw.text((10, 10), text, fill=(255, 255, 255))

        return img

    def grow_image(self, stages=5, start_size=256, growth_factor=2, palette="fire",
                   max_iter_base=100, zoom_progression=True):
        """
        Generate progressively growing images.

        Args:
            stages: Number of growth stages
            start_size: Initial image size
            growth_factor: Size multiplier per stage
            palette: Color palette
            max_iter_base: Base iteration count
            zoom_progression: Whether to zoom in progressively

        Returns:
            List of generated image paths
        """
        print("🚀 IMAGE GROWTH EXPERIMENT - INITIATING")
        print("=" * 60)

        generated_images = []

        for stage in range(1, stages + 1):
            # Calculate parameters for this stage
            size = int(start_size * (growth_factor ** (stage - 1)))
            max_iter = max_iter_base + (stage - 1) * 50
            zoom = 1 + (stage - 1) * 0.5 if zoom_progression else 1

            print(f"\n📈 Stage {stage}/{stages}")
            print(f"   Size: {size}x{size}px")
            print(f"   Iterations: {max_iter}")
            print(f"   Zoom: {zoom:.2f}x")
            print(f"   Generating...", end=" ", flush=True)

            # Generate fractal
            start_time = time.time()
            fractal_data = self.mandelbrot(size, size, max_iter=max_iter, zoom=zoom)

            # Create image
            img = self.create_colorful_image(fractal_data, size, size, palette=palette)

            generation_time = time.time() - start_time

            # Add metadata
            img = self.add_metadata_overlay(img, stage, size, generation_time)

            # Save image
            filename = f"growth_stage_{stage:02d}_{size}x{size}.png"
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath, optimize=True)
            generated_images.append(filepath)

            print(f"✓ Completed in {generation_time:.2f}s")
            print(f"   Saved: {filename}")
            print(f"   File size: {os.path.getsize(filepath) / 1024:.1f} KB")

        print("\n" + "=" * 60)
        print("✨ GROWTH COMPLETE - DOUBTS SHATTERED ✨")
        print(f"Generated {stages} stages of exponential image growth!")
        print(f"Total images: {len(generated_images)}")
        print(f"Output directory: {self.output_dir}")

        return generated_images

    def create_growth_comparison(self, image_paths):
        """Create a comparison image showing all growth stages."""
        print("\n🎨 Creating growth comparison montage...")

        # Load all images
        images = [Image.open(path) for path in image_paths]

        # Calculate montage size (arrange in a row)
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)

        # For large images, scale down for comparison
        if total_width > 8000:
            scale_factor = 8000 / total_width
            images = [img.resize((int(img.width * scale_factor),
                                 int(img.height * scale_factor)),
                                Image.Resampling.LANCZOS) for img in images]
            total_width = sum(img.width for img in images)
            max_height = max(img.height for img in images)

        # Create montage
        montage = Image.new('RGB', (total_width, max_height), color=(0, 0, 0))

        x_offset = 0
        for img in images:
            montage.paste(img, (x_offset, 0))
            x_offset += img.width

        # Save montage
        montage_path = os.path.join(self.output_dir, "growth_comparison.png")
        montage.save(montage_path, optimize=True)

        print(f"✓ Comparison montage saved: growth_comparison.png")
        print(f"   Size: {montage.width}x{montage.height}px")

        return montage_path


def main():
    """Main execution function."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        IMAGE GROWTH EXPERIMENT                          ║
    ║        Shattering Doubts Edition                        ║
    ║                                                          ║
    ║        "Watch complexity emerge from simplicity"        ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Initialize engine
    engine = ImageGrowthEngine(output_dir="output")

    # Configuration
    print("Configuration:")
    print("  • Starting size: 256x256px")
    print("  • Growth factor: 2x per stage")
    print("  • Stages: 6")
    print("  • Palette: Psychedelic")
    print("  • Progressive zoom: Enabled")
    print()

    # Generate growing images
    image_paths = engine.grow_image(
        stages=6,
        start_size=256,
        growth_factor=2,
        palette="psychedelic",
        max_iter_base=100,
        zoom_progression=True
    )

    # Create comparison montage
    engine.create_growth_comparison(image_paths)

    print("\n" + "=" * 60)
    print("🎯 MISSION ACCOMPLISHED")
    print("=" * 60)
    print(f"✓ {len(image_paths)} stages generated")
    print(f"✓ Maximum resolution: {2**5 * 256}x{2**5 * 256}px (8192x8192!)")
    print("✓ Comparison montage created")
    print(f"✓ All files saved to: output/")
    print("\n💥 DOUBTS = SHATTERED 💥\n")


if __name__ == "__main__":
    main()
