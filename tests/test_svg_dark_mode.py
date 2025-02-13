import unittest
import os
import shutil
from svg_dark_mode import add_dark_mode_attributes, process_svg_file, process_folder

class TestSVGDarkMode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before all tests."""
        cls.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.source_dir = os.path.join(cls.project_root, 'original_icons')
        cls.output_dir = os.path.join(cls.project_root, 'dark_mode_icons')
        
        # Create output directory if it doesn't exist
        os.makedirs(cls.output_dir, exist_ok=True)
        cls._clean_output_dir()
        
        # Sample SVG for content tests
        cls.sample_svg = '''<svg width="100" height="100">
            <rect fill="black" width="50" height="50"/>
            <circle fill="white" cx="75" cy="75" r="20"/>
        </svg>'''
        
        # Verify source directory exists and contains SVG files
        if not os.path.exists(cls.source_dir):
            raise ValueError(f"Source directory {cls.source_dir} does not exist")
        if not any(f.endswith('.svg') for f in os.listdir(cls.source_dir)):
            raise ValueError(f"No SVG files found in {cls.source_dir}")

    @classmethod
    def _clean_output_dir(cls):
        """Helper method to clean output directory contents."""
        if os.path.exists(cls.output_dir):
            for file in os.listdir(cls.output_dir):
                file_path = os.path.join(cls.output_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def setUp(self):
        """Set up test fixtures before each test method."""
        self._clean_output_dir()

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        self._clean_output_dir()

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures after all tests."""
        cls._clean_output_dir()

    def test_add_dark_mode_attributes(self):
        """Test the add_dark_mode_attributes function with first SVG from original_icons."""
        source_files = [f for f in os.listdir(self.source_dir) if f.endswith('.svg')]
        if not source_files:
            self.skipTest("No SVG files found in original_icons directory")
        
        # Read the first SVG file for testing
        with open(os.path.join(self.source_dir, source_files[0]), 'r', encoding='utf-8') as f:
            original_svg = f.read()
        
        print(f"\nTesting with file: {source_files[0]}")
        print(f"Original SVG:\n{original_svg[:200]}...")
        
        result = add_dark_mode_attributes(original_svg)
        print(f"\nModified SVG:\n{result[:200]}...")
        
        # Verify modifications
        self.assertNotIn('<style>', result)
        self.assertTrue(
            'fill="black" fill-dark="white"' in result or
            'fill="white" fill-dark="black"' in result
        )

    def test_process_svg_file(self):
        """Test processing of a single SVG file from original_icons."""
        source_files = [f for f in os.listdir(self.source_dir) if f.endswith('.svg')]
        if not source_files:
            self.skipTest("No SVG files found in original_icons directory")
        
        source_file = os.path.join(self.source_dir, source_files[0])
        output_file = os.path.join(self.output_dir, source_files[0])
        
        process_svg_file(source_file, output_file)
        
        # Verify the output file
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertNotIn('<style>', content)
            self.assertTrue(
                'fill="black" fill-dark="white"' in content or
                'fill="white" fill-dark="black"' in content
            )

    def test_process_folder(self):
        """Test processing of all SVG files in original_icons."""
        print("\nTesting process_folder:")
        source_files = [f for f in os.listdir(self.source_dir) if f.endswith('.svg')]
        if not source_files:
            self.skipTest("No SVG files found in original_icons directory")
        
        print(f"Source directory: {self.source_dir}")
        print(f"Found {len(source_files)} SVG files")
        
        process_folder(self.source_dir, self.output_dir)
        
        # Verify all files were processed
        processed_files = [f for f in os.listdir(self.output_dir) if f.endswith('.svg')]
        self.assertEqual(set(source_files), set(processed_files))
        
        # Check each processed file
        print("\nVerifying processed files:")
        for filename in processed_files:
            with open(os.path.join(self.output_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertNotIn('<style>', content)
                self.assertTrue(
                    'fill="black" fill-dark="white"' in content or
                    'fill="white" fill-dark="black"' in content
                )
                print(f"✓ {filename}: Dark mode attributes verified")

    def test_invalid_folder(self):
        """Test handling of invalid folder paths."""
        with self.assertRaises(ValueError):
            process_folder('/nonexistent/path', self.output_dir)

    def test_invalid_svg_content(self):
        """Test handling of invalid SVG content."""
        invalid_svg = '<not-valid-svg>'
        result = add_dark_mode_attributes(invalid_svg)
        self.assertEqual(result, invalid_svg)  # Should return unchanged

    def test_svg_with_existing_style(self):
        """Test handling SVG with existing style tag."""
        svg_with_style = '''<svg width="100" height="100">
            <style>.existing{color:blue}</style>
            <path fill="black" d="M0 0h24v24H0z"/>
        </svg>'''
        result = add_dark_mode_attributes(svg_with_style)
        
        # Verify existing style is preserved
        self.assertIn('.existing{color:blue}', result)
        
        # Verify dark mode attributes are added
        self.assertIn('fill="black" fill-dark="white"', result)
        
        # Verify original style tag structure
        self.assertIn('<style>', result)
        self.assertIn('</style>', result)

    def test_hex_color_conversion(self):
        """Test handling of hex color values."""
        hex_svg = '<path fill="#000000"/><path fill="#FFFFFF"/>'
        result = add_dark_mode_attributes(hex_svg)
        self.assertIn('fill="black" fill-dark="white"', result)
        self.assertIn('fill="white" fill-dark="black"', result)

if __name__ == '__main__':
    unittest.main()
