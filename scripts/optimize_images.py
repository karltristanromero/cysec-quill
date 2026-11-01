#!/usr/bin/env python3
"""
optimize_images.py — Compresses and optimizes screenshot images (.png, .jpg)
stored inside writeup assets/ subdirectories to keep Git history lightweight.

Usage:
    python3 scripts/optimize_images.py [--max-width 1920] [--quality 85]
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow (PIL) is required. Install via: pip install Pillow")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent


def optimize_file(img_path: Path, max_width: int, quality: int) -> tuple[int, int]:
    original_size = img_path.stat().st_size
    try:
        with Image.open(img_path) as im:
            fmt = im.format
            width, height = im.size

            # Resize if larger than max_width
            if width > max_width:
                new_height = int(height * (max_width / width))
                im = im.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Optimize according to format
            if fmt == "PNG":
                im.save(img_path, format="PNG", optimize=True)
            elif fmt in ("JPEG", "JPG"):
                im.save(img_path, format="JPEG", quality=quality, optimize=True)
            else:
                return original_size, original_size

        new_size = img_path.stat().st_size
        return original_size, new_size
    except Exception as e:
        print(f"Skipping {img_path.name}: {e}")
        return original_size, original_size


def main():
    parser = argparse.ArgumentParser(description="Optimize screenshots and diagrams in writeup assets directories.")
    parser.add_argument("--max-width", type=int, default=1920, help="Maximum image width in pixels (default: 1920)")
    parser.add_argument("--quality", type=int, default=85, help="JPEG quality factor (default: 85)")
    args = parser.parse_args()

    asset_dirs = list(REPO_ROOT.glob("docs/**/assets")) + list(REPO_ROOT.glob("drafts/**/assets"))
    image_files = []
    for ad in asset_dirs:
        for f in ad.iterdir():
            if f.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                image_files.append(f)

    if not image_files:
        print("No image assets found to optimize.")
        sys.exit(0)

    print(f"Image Optimizer: Scanning {len(image_files)} asset image(s)...")

    total_orig = 0
    total_opt = 0

    for img in image_files:
        orig, opt = optimize_file(img, args.max_width, args.quality)
        total_orig += orig
        total_opt += opt
        diff = orig - opt
        if diff > 1024:
            print(f"  Optimized {img.name}: {orig / 1024:.1f} KB -> {opt / 1024:.1f} KB (saved {diff / 1024:.1f} KB)")

    saved_mb = (total_orig - total_opt) / (1024 * 1024)
    print(f"\nOptimization complete: Total saved: {saved_mb:.2f} MB.")


if __name__ == "__main__":
    main()
