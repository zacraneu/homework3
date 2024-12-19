import unittest
import subprocess
import os


class TestConfigLanguage(unittest.TestCase):

    def run_config(self, input_xml):
        # Записываем входные данные в файл
        temp_file = "temp_input.xml"
        with open(temp_file, "w") as f:
            f.write(input_xml)
        
        # Запускаем subprocess
        result = subprocess.run(
            ['python', 'config_language.py', temp_file],
            capture_output=True, text=True
        )
        
        # Удаляем временный файл
        os.remove(temp_file)
        
        return result.stdout.strip()

    def test_basic_definition(self):
        input_xml = '''<config>
            <define name="x" value="10"/>
        </config>'''

        expected_output = '''{
x = 10;
}'''

        output = self.run_config(input_xml)
        self.assertEqual(output, expected_output)

    def test_basic_operation(self):
        input_xml = '''<config>
            <operation operation="+">
                <value>5</value>
                <value>3</value>
            </operation>
        </config>'''

        expected_output = '''{
8;
}'''

        output = self.run_config(input_xml)
        self.assertEqual(output, expected_output)

    def test_definition_and_operation(self):
        input_xml = '''<config>
            <define name="x" value="10"/>
            <operation operation="+">
                <value>5</value>
                <value>3</value>
            </operation>
        </config>'''

        expected_output = '''{
x = 10;
8;
}'''

        output = self.run_config(input_xml)
        self.assertEqual(output, expected_output)

    def test_nested_operations(self):
        input_xml = '''<config>
            <define name="x" value="10"/>
            <operation operation="-">
                <value>x</value>
                <operation operation="+">
                    <value>2</value>
                    <value>3</value>
                </operation>
            </operation>
        </config>'''

        expected_output = '''{
x = 10;
5;
}'''

        output = self.run_config(input_xml)
        self.assertEqual(output, expected_output)

    def test_multiple_definitions_and_operations(self):
        input_xml = '''<config>
            <define name="x" value="10"/>
            <define name="y" value="20"/>
            <operation operation="+">
                <value>x</value>
                <value>5</value>
            </operation>
            <operation operation="mod">
                <value>y</value>
                <value>6</value>
            </operation>
        </config>'''

        expected_output = '''{
x = 10;
y = 20;
15;
2;
}'''

        output = self.run_config(input_xml)
        self.assertEqual(output, expected_output)

    def test_complex_example(self):
        input_xml = '''<config>
            <define name="a" value="100"/>
            <operation operation="-">
                <value>a</value>
                <operation operation="+">
                    <value>20</value>
                    <value>30</value>
                </operation>
            </operation>
            <operation operation="mod">
                <value>a</value>
                <value>9</value>
            </operation>
        </config>'''

        expected_output = '''{
a = 100;
50;
1;
}'''

        output = self.run_config(input_xml)
        self.assertEqual(output, expected_output)

    def test_value_only(self):
        input_xml = '''<config>
            <value>42</value>
        </config>'''

        expected_output = '''{
42;
}'''

        output = self.run_config(input_xml)
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
