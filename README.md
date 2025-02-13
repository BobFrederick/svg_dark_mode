# SVG Dark Mode Converter

A command-line utility that adds dark mode support to SVG files by automatically inserting fill attributes for both light and dark themes.

## Features

- Processes entire folders of SVG files
- Adds dark mode support through fill attributes
- Automatically inverts colors for dark mode
- Handles hex colors (#RRGGBB), named colors, and common color mappings
- No external dependencies required

## How It Works

The script modifies SVG files by adding dark mode fill attributes with inverted colors:

```xml
<!-- Original SVG -->
<path fill="#FF0000"/>
<path fill="blue"/>

<!-- Modified SVG -->
<path fill="#FF0000" fill-dark="#00FFFF"/>
<path fill="blue" fill-dark="#FFFF00"/>
```

The script handles:
- Hex colors (#RRGGBB) - automatically inverted
- Named colors - using predefined mappings
- Preserves existing non-color styles

## Usage

1. Prepare your SVG files in a source folder
2. Run the script:
    ```bash
    python3 svg_dark_mode.py source_folder destination_folder
    ```
3. Find the converted files in your specified destination folder

Example with separate folders:
```bash
python3 svg_dark_mode.py ./original_icons ./dark_mode_icons
```

To overwrite files in place, use the same path for source and destination:
```bash
python3 svg_dark_mode.py ./my_icons ./my_icons
```

**Note:** When using the same path for source and destination, the original files will be overwritten with the dark mode versions. Make sure to backup your files if needed.

## Requirements

- Python 3.x
- No additional packages required

## Testing

To run the unit tests:

```bash
python -m unittest discover tests
```

The test suite includes:
- File processing validation
- Dark mode attribute verification
- Error handling cases
- Directory processing tests

For contributors adding new features, please ensure all tests pass before submitting changes.

## Notes
Thanks to Callum Sykes from McNeel for the recommendation on the color conversion method. For more details, visit [this discussion](https://discourse.mcneel.com/t/changing-dark-mode-icon-setting-doesnt-stick-the-first-time/193038/7?u=bfrederick).

## License

MIT License