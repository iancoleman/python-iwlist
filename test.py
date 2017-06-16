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

    def tearDown(self):
        self.cases = []

    def test_parse_length(self):
        for case in self.cases:
            self.assertEqual(len(case["expected"]), len(case["parsed"]))

    def test_cells_have_all_expected_keys(self):
        for case in self.cases:
            for i in range(len(case["expected"])):
                e = case["expected"][i]
                p = case["parsed"][i]
                for key in e:
                    msg = "\nkey is in expected but missing in parsed:\nkey: %s\ntestdir: %s\ncellnumber: %s" % (key, case["name"], e["cellnumber"])
                    self.assertTrue(key in p, msg)

    def test_cells_dont_have_extra_keys(self):
        for case in self.cases:
            for i in range(len(case["expected"])):
                e = case["expected"][i]
                p = case["parsed"][i]
                for key in p:
                    msg = "\nkey was parsed but missing in expected:\nkey: %s\ntestdir: %s\ncellnumber: %s" % (key, case["name"], e["cellnumber"])
                    self.assertTrue(key in e, msg)

    def test_cells_have_expected_values(self):
        for case in self.cases:
            for i in range(len(case["expected"])):
                e = case["expected"][i]
                for k in e:
                    ev = e[k]
                    pv = case["parsed"][i][k]
                    msg = "\nwrong value for field:\ntestdir: %s\nfield: %s\ncellnumber: %s\nexpected: %s\nactual: %s" % (case["name"], k, e["cellnumber"], ev, pv)
                    self.assertTrue(ev == pv, msg)

if __name__ == '__main__':
    unittest.main()
