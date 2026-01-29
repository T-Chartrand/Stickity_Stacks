"""
Stickity Stacks - Icon Converter
Converts PNG to Windows ICO format with multiple resolutions
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("PIL/Pillow not installed!")
    print("Install with: pip install Pillow")
    sys.exit(1)

def create_ico(png_path, ico_path=None, sizes=None):
    """
    Convert PNG to ICO with multiple resolutions
    
    Args:
        png_path: Path to input PNG file
        ico_path: Path to output ICO file (optional)
        sizes: List of sizes to include (default: common Windows sizes)
    """
    if sizes is None:
        # Standard Windows icon sizes
        sizes = [256, 128, 64, 48, 32, 16]
    
    png_file = Path(png_path)
    if not png_file.exists():
        print(f"Error: {png_path} not found!")
        return False
    
    if ico_path is None:
        ico_path = png_file.with_suffix('.ico')
    else:
        ico_path = Path(ico_path)
    
    try:
        # Open source image
        img = Image.open(png_file)
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create list of resized images
        icon_sizes = []
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            icon_sizes.append(resized)
        
        # Save as ICO
        icon_sizes[0].save(
            ico_path,
            format='ICO',
            sizes=[(size, size) for size in sizes],
            append_images=icon_sizes[1:]
        )
        
        print(f"✓ Created: {ico_path}")
        print(f"  Sizes: {', '.join(map(str, sizes))}px")
        print(f"  File size: {ico_path.stat().st_size / 1024:.2f} KB")
        
        return True
        
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

def main():
    """Main entry point"""
    
    print("=" * 50)
    print("  Stickity Stacks - Icon Converter")
    print("=" * 50)
    print()
    
    # Default paths
    default_png = Path(__file__).parent.parent / 'stickity_stacks.png'
    default_ico = Path(__file__).parent.parent / 'stickity_stacks.ico'
    
    # Get input file
    if len(sys.argv) > 1:
        png_path = Path(sys.argv[1])
    else:
        png_path = default_png
    
    # Get output file
    if len(sys.argv) > 2:
        ico_path = Path(sys.argv[2])
    else:
        ico_path = default_ico
    
    print(f"Input PNG:  {png_path}")
    print(f"Output ICO: {ico_path}")
    print()
    
    # Convert
    success = create_ico(png_path, ico_path)
    
    if success:
        print()
        print("=" * 50)
        print("  Next steps:")
        print("=" * 50)
        print()
        print("1. Update build_installer.spec:")
        print("   icon='stickity_stacks.ico',")
        print()
        print("2. Update installer.iss:")
        print("   SetupIconFile=stickity_stacks.ico")
        print()
        print("3. Rebuild:")
        print("   build_complete.bat")
        print()
        return 0
    else:
        print()
        print("Icon creation failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
