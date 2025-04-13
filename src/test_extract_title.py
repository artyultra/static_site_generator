import unittest

from main import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_header_at_top(self):
        md = """# h1 header

## h2 header

### h3 header"""
        header = extract_title(md)
        self.assertEqual(header, "h1 header")

    def test_header_at_middle(self):
        md = """## h2 header

# h1 header

### h3 header"""
        header = extract_title(md)
        self.assertEqual(header, "h1 header")

    def test_no_header_text(self):
        md = """## h2 header

# 

### h3 header"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found")

    def test_no_header_provided(self):
        md = """## h2 header

### h3 header"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found")


if __name__ == "__main__":
    unittest.main()
