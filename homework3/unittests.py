import unittest
from io import StringIO
import os

from hw3 import remove_comments, parse_dictionaries, parse_constants, evaluate_expression, generate_xml, process_file

class TestConfigParser(unittest.TestCase):

    def test_remove_comments(self):
        text_with_comments = """
        Some text here
{{!-- This is a comment --}}More text
        {{!-- Another comment --}}
        """
        result = remove_comments(text_with_comments)
        expected = "Some text here\nMore text"
        self.assertEqual(result, expected)

    def test_parse_dictionaries(self):
        text_with_dicts = """
        begin dict1
            key1 := value1;
            key2 := value2;
        end
        begin dict2
            keyA := valueA;
            keyB := valueB;
        end
        """
        dictionaries, remaining_text = parse_dictionaries(text_with_dicts)
        expected_dictionaries = [
            {'key1': 'value1', 'key2': 'value2'},
            {'keyA': 'valueA', 'keyB': 'valueB'}
        ]
        self.assertEqual(dictionaries, expected_dictionaries)
        self.assertEqual(remaining_text.strip(), "")

    def test_parse_constants(self):
        text_with_constants = """
        var x = 10;
        var y = |x 5 +|;
        var z = 20;
        """
        constants, remaining_text = parse_constants(text_with_constants)
        expected_constants = {'x': 10, 'y': 15, 'z': 20}
        self.assertEqual(constants, expected_constants)
        self.assertEqual(remaining_text.strip(), "")

    def test_evaluate_expression(self):
        constants = {'x': 10, 'y': 5}
        expression = "x y +"
        result = evaluate_expression(expression, constants)
        self.assertEqual(result, 15)

        expression_with_mod = "x y mod(3) +"
        result = evaluate_expression(expression_with_mod, constants)
        self.assertEqual(result, 12)

    def test_generate_xml(self):
        dictionaries = [{'key1': 'value1', 'key2': 'value2'}]
        constants = {'x': 10, 'y': 15}
        expected_xml = '''<?xml version="1.0" ?>
<root>
    <constants>
        <constant name="x">10</constant>
        <constant name="y">15</constant>
    </constants>
    <dictionaries>
        <dictionary>
            <entry name="key1">value1</entry>
            <entry name="key2">value2</entry>
        </dictionary>
    </dictionaries>
</root>
'''
        result_xml = generate_xml(dictionaries, constants)
        self.assertEqual(result_xml, expected_xml)

    def test_process_file(self):
        # Mock input data
        mock_file_content = """
        {{!-- comment --}}
        begin dict1
            key1 := value1;
            key2 := value2;
        end
        var x = 10;
        var y = |x 5 +|;
        """
        mock_input_file = "test_file.txt"
        with open(mock_input_file, 'w') as file:
            file.write(mock_file_content)
        
        try:
            xml_output = process_file(mock_input_file)
            self.assertIn("<constant name=\"x\">10</constant>", xml_output)
            self.assertIn("<entry name=\"key1\">value1</entry>", xml_output)
        finally:
            os.remove(mock_input_file)  # Cleanup the test file

if __name__ == '__main__':
    unittest.main()
