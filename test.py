import json
import iwlist
import unittest

def fileContent(filename):
    f = open(filename)
    content = f.read()
    f.close()
    return content

class TestParse(unittest.TestCase):

    def setUp(self):
        self.parsed = iwlist.parse(fileContent("test/scan.txt"))
        self.expected = json.loads(fileContent("test/vectors.json"))

    def test_parse_length(self):
        self.assertEqual(len(self.expected), len(self.parsed))

    def test_cells_have_all_expected_keys(self):
        for i in range(len(self.expected)):
            e = self.expected[i]
            p = self.parsed[i]
            for key in e:
                self.assertTrue(key in p)

    def test_cells_dont_have_extra_keys(self):
        for i in range(len(self.expected)):
            e = self.expected[i]
            p = self.parsed[i]
            for key in p:
                self.assertTrue(key in e)

if __name__ == '__main__':
    unittest.main()
