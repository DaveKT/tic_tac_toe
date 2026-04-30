import os
import sys
import json
import pathlib
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stats import StatsTracker


class TestStatsTracker(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._path = pathlib.Path(self._tmpdir.name) / "stats.json"

    def tearDown(self):
        self._tmpdir.cleanup()

    def _tracker(self):
        t = StatsTracker(self._path)
        t.load()
        return t

    def test_initial_zeros(self):
        t = self._tracker()
        self.assertEqual(t.x_wins, 0)
        self.assertEqual(t.o_wins, 0)
        self.assertEqual(t.draws, 0)

    def test_record_x_win(self):
        t = self._tracker()
        t.record("X")
        self.assertEqual(t.x_wins, 1)
        self.assertEqual(t.o_wins, 0)
        self.assertEqual(t.draws, 0)

    def test_record_o_win(self):
        t = self._tracker()
        t.record("O")
        self.assertEqual(t.x_wins, 0)
        self.assertEqual(t.o_wins, 1)
        self.assertEqual(t.draws, 0)

    def test_record_draw(self):
        t = self._tracker()
        t.record("draw")
        self.assertEqual(t.x_wins, 0)
        self.assertEqual(t.o_wins, 0)
        self.assertEqual(t.draws, 1)

    def test_persist_across_instances(self):
        t1 = self._tracker()
        t1.record("X")
        t1.record("O")
        t1.record("draw")

        t2 = self._tracker()
        self.assertEqual(t2.x_wins, 1)
        self.assertEqual(t2.o_wins, 1)
        self.assertEqual(t2.draws, 1)

    def test_reset_zeros_and_saves(self):
        t1 = self._tracker()
        t1.record("X")
        t1.record("X")
        t1.reset()
        self.assertEqual(t1.x_wins, 0)

        t2 = self._tracker()
        self.assertEqual(t2.x_wins, 0)
        self.assertEqual(t2.o_wins, 0)
        self.assertEqual(t2.draws, 0)

    def test_load_missing_file_no_crash(self):
        missing = pathlib.Path(self._tmpdir.name) / "nonexistent.json"
        t = StatsTracker(missing)
        t.load()
        self.assertEqual(t.x_wins, 0)
        self.assertEqual(t.o_wins, 0)
        self.assertEqual(t.draws, 0)

    def test_load_corrupt_json_no_crash(self):
        self._path.write_text("not valid json {{{")
        t = self._tracker()
        self.assertEqual(t.x_wins, 0)
        self.assertEqual(t.o_wins, 0)
        self.assertEqual(t.draws, 0)

    def test_load_partial_keys(self):
        self._path.write_text(json.dumps({"x_wins": 3}))
        t = self._tracker()
        self.assertEqual(t.x_wins, 3)
        self.assertEqual(t.o_wins, 0)
        self.assertEqual(t.draws, 0)

    def test_atomic_save_no_leftover_tmp(self):
        t = self._tracker()
        t.record("X")
        tmp = self._path.with_suffix(".json.tmp")
        self.assertFalse(tmp.exists())


if __name__ == "__main__":
    unittest.main()
