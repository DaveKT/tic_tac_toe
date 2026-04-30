import json
import pathlib

_STATS_FILE = pathlib.Path(__file__).parent / "stats.json"
_KEYS = ("x_wins", "o_wins", "draws")


class StatsTracker:
    def __init__(self, path: pathlib.Path = _STATS_FILE):
        self._path = path
        self._counts = dict.fromkeys(_KEYS, 0)

    def load(self) -> None:
        try:
            data = json.loads(self._path.read_text())
            for k in _KEYS:
                v = data.get(k, 0)
                self._counts[k] = v if isinstance(v, int) else 0
        except Exception:
            self._counts = dict.fromkeys(_KEYS, 0)

    def save(self) -> None:
        tmp = self._path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self._counts, indent=2))
        tmp.replace(self._path)

    def record(self, result: str) -> None:
        key = {"X": "x_wins", "O": "o_wins", "draw": "draws"}[result]
        self._counts[key] += 1
        self.save()

    def reset(self) -> None:
        self._counts = dict.fromkeys(_KEYS, 0)
        self.save()

    @property
    def x_wins(self) -> int: return self._counts["x_wins"]

    @property
    def o_wins(self) -> int: return self._counts["o_wins"]

    @property
    def draws(self) -> int: return self._counts["draws"]
