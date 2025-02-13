"""
svg_dark_mode.py

A script to add dark mode attributes to SVG files.

This script processes SVG files by adding custom attributes to support dark mode.
It can process individual SVG files or all SVG files within a specified directory.

Usage:
    python svg_dark_mode.py source_folder dest_folder

Modules:
    os
    sys
    re

Functions:
    add_dark_mode_attributes(svg_content)
    process_svg_file(source_path, dest_path)
    process_folder(source_folder, dest_folder)
    main()

Exceptions:
    IOError
    UnicodeDecodeError
    ValueError

Encoding:
    UTF-8
"""

import os
import sys
import re
import colorsys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def invert_color(color):
    """
    Invert a color for dark mode.
    Handles both hex (#RRGGBB) and named colors.
    """
    # Color name mapping
    color_map = {
        'black': 'white',
        'white': 'black',
        # Add more common color mappings as needed
    }
    
    # Handle named colors
    if color.lower() in color_map:
        return color_map[color.lower()]
    
    # Handle hex colors
    if color.startswith('#'):
        rgb = hex_to_rgb(color)
        inverted = tuple(255 - c for c in rgb)
        return rgb_to_hex(inverted)
    
    return color


def add_dark_mode_attributes(svg_content):
    """
    Add dark mode attributes to SVG content.

    Args:
        svg_content (str): The raw SVG file content as a string.

    Returns:
        str: Modified SVG content with dark mode attributes.

    Examples:
        ```python
        svg_content = '<path fill="#000000"/>'
        modified = add_dark_mode_attributes(svg_content)
        # Results in: '<path fill="black" fill-dark="white"/>'
        ```
    """
    print("Original content:")
    print(svg_content[:200])  # Debug print
    
    # Extract and preserve existing styles that aren't related to dark mode
    style_pattern = r'<style>(.*?)</style>'
    existing_styles = re.findall(style_pattern, svg_content, re.DOTALL)
    preserved_styles = []
    
    for style in existing_styles:
        # Keep styles that don't contain dark mode or fill related rules
        if not any(keyword in style.lower() for keyword in ['@media', 'fill:', 'dark']):
            preserved_styles.append(style)
    
    # Remove all style tags first
    content = re.sub(style_pattern, '', svg_content, flags=re.DOTALL)
    
    # Remove any existing dark mode attributes
    content = re.sub(r'fill-dark="[^"]*"', '', content)
    content = re.sub(r'fill-light="[^"]*"', '', content)
    
    # Find all fill attributes and add dark mode versions
    def replace_fill(match):
        fill = match.group(1)
        dark_fill = invert_color(fill)
        return f'fill="{fill}" fill-dark="{dark_fill}"'
    
    # Handle both hex and named colors
    content = re.sub(r'fill="([^"]*)"(?!\s+fill-dark)', replace_fill, content)
    
    # Reinsert preserved styles after svg tag
    if preserved_styles:
        style_block = f'<style>{" ".join(preserved_styles)}</style>'
        svg_end = content.find('>')
        content = content[:svg_end + 1] + style_block + content[svg_end + 1:]
    
    print("\nFinal content:")
    print(content[:200])  # Debug print
    return content


def process_svg_file(source_path, dest_path):
    """
    Process a single SVG file by adding dark mode attributes.

    Args:
        source_path (str): Path to the source SVG file.
        dest_path (str): Path where the modified SVG file will be saved.

    Raises:
        IOError: If the file cannot be read or written.
        UnicodeDecodeError: If the file is not properly UTF-8 encoded.

    Examples:
        ```python
        process_svg_file("path/to/source/icon.svg", "path/to/dest/icon.svg")
        ```
    """
    try:
        with open(source_path, "r", encoding="utf-8") as file:
            svg = file.read()
            print(f"\nProcessing file: {source_path}")
        modified_svg = add_dark_mode_attributes(svg)
        
        # Verify no style tags exist in output
        if '<style>' in modified_svg:
            print("Warning: Style tags found in output!")
            
        with open(dest_path, "w", encoding="utf-8") as file:
            file.write(modified_svg)
            
    except (IOError, UnicodeDecodeError) as e:
        print(f"IO Error processing {source_path}: {str(e)}")
        raise
    except UnicodeDecodeError as e:
        print(f"Encoding error in {source_path}: {str(e)}")
        print("Please ensure the file is properly UTF-8 encoded")
        raise


def process_folder(source_folder, dest_folder):
    """
    Process all SVG files from source folder to destination folder.

    Args:
        source_folder (str): Path to the folder containing source SVG files.
        dest_folder (str): Path to the folder where modified files will be saved.

    Raises:
        ValueError: If the source path is not a valid directory.
        IOError: If there are issues accessing files or creating directories.

    Examples:
        ```python
        process_folder("path/to/source/folder", "path/to/dest/folder")
        ```
    """
    if not os.path.isdir(source_folder):
        raise ValueError("Source path is not a valid directory")

    # Create destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)
    
    errors = []
    for filename in os.listdir(source_folder):
        if filename.endswith(".svg"):
            source_path = os.path.join(source_folder, filename)
            dest_path = os.path.join(dest_folder, filename)
            try:
                process_svg_file(source_path, dest_path)
                print(f"Successfully processed: {filename}")
            except (IOError, UnicodeDecodeError) as e:
                errors.append((filename, str(e)))
                continue
    
    if errors:
        print("\nThe following files had errors:")
        for filename, error in errors:
            print(f"- {filename}: {error}")
        raise ValueError(f"Failed to process {len(errors)} files")


def main():
    """
    Main entry point for the script.

    Processes command line arguments and initiates SVG processing.
    Exits with status code 1 if invalid arguments are provided or errors occur.

    Usage:
        ```bash
        python svg_dark_mode.py source_folder dest_folder
        ```
    """
    if len(sys.argv) != 3:
        print("Usage: python3 svg_dark_mode.py source_folder dest_folder")
        sys.exit(1)
    
    try:
        process_folder(sys.argv[1], sys.argv[2])
        print("\nAll files processed successfully!")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
