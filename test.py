import json
import os
import iwlist
import unittest

def fileContent(filename):
    f = open(filename)
    content = f.read()
    f.close()
    return content

class TestParse(unittest.TestCase):

    def setUp(self):
        dirs = os.listdir("test")
        self.cases = []
        for d in dirs:
            scanFile = os.path.join("test", d, "scan.txt")
            vectorsFile = os.path.join("test", d, "vectors.json")
            case = {
                    "name": d,
                    "parsed": iwlist.parse(fileContent(scanFile)),
                    "expected": json.loads(fileContent(vectorsFile)),
                }
            self.cases.append(case)

    def test_parse_length(self):
        for case in self.cases:
            self.assertEqual(len(case["expected"]), len(case["parsed"]))

    def test_cells_have_all_expected_keys(self):
        for case in self.cases:
            for i in range(len(case["expected"])):
                e = case["expected"][i]
                p = case["parsed"][i]
                for key in e:
                    msg = "key missing: %s\n%s\ncellnumber: %s" % (key, case["name"], e["cellnumber"])
                    self.assertTrue(key in p, msg)

    def test_cells_dont_have_extra_keys(self):
        for case in self.cases:
            for i in range(len(case["expected"])):
                e = case["expected"][i]
                p = case["parsed"][i]
                for key in p:
                    self.assertTrue(key in e)

if __name__ == '__main__':
    unittest.main()
