"""Input safety and portable request generation only; this does not verify Adobe rendering."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('lab_build',BASE/'scripts/build.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class Requests(unittest.TestCase):
    def test_all_examples_generate_with_no_unexpanded_tokens(self):
        for p in (BASE/'examples').glob('*.json'):
            with self.subTest(p=p.name),tempfile.TemporaryDirectory() as out:
                script=mod.build(json.loads(p.read_text()),out).read_text()
                self.assertNotIn('__CONFIG__',script);self.assertNotIn('__OUTPUT__',script)
                self.assertIn('valueAtTime',script)
    def test_invalid_requests_fail_before_output(self):
        for change in [{'fps':0},{'count':1.2},{'width':True},{'duration':float('nan')},{'color':[1,2,0]},
                       {'asset':'Z:/missing-input.png'},{'name':'bad";$.evalFile("other")'},
                       {'count':100,'delay_frames':30},{'unexpected':1}]:
            with self.subTest(change=change),self.assertRaises(ValueError):mod.validate(change)
    def test_stale_run_is_rejected(self):
        with tempfile.TemporaryDirectory() as out:
            mod.build({},out)
            with self.assertRaises(FileExistsError):mod.build({},out)

if __name__=='__main__':unittest.main()
