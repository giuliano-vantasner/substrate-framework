"""Assembles attempt 0044 final numbers from committed artifacts."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out = {}
    out["derivation"] = json.loads((HERE / "derivation-results.json").read_text())
    clean = json.loads((HERE / "clean-ladder-state.json").read_text())
    out["clean_ladder"] = [
        {k: v for k, v in r.items() if k != "values"} | {"values": r["values"]}
        for r in clean["ladder"]
    ]
    if (HERE / "stability-windows-clean.json").exists():
        out["stability_windows"] = json.loads((HERE / "stability-windows-clean.json").read_text())
    if (HERE / "debox-results.json").exists():
        out["low_R"] = json.loads((HERE / "low-R-clean.json").read_text())
    if (HERE / "free_wall" .exists() if False else (HERE / "debox-results.json").exists()):
        fw = json.loads((HERE / "debox-results.json").read_text())
        out["free_wall_R8"] = fw.get("free_wall_R8")
    # self-consistency verdict per background
    verdicts = []
    wins = {w["radius"]: w.get("crossing_radii", []) for w in out.get("stability_windows", [])}
    for row in out["clean_ladder"]:
        R = row["radius"]
        cr = sorted(wins.get(R, []))
        if len(cr) >= 2:
            inside = cr[0] < R < cr[-1]
            verdicts.append({"radius": R, "window": [cr[0], cr[-1]],
                             "self_consistent_stable": bool(inside)})
        else:
            verdicts.append({"radius": R, "window": None,
                             "self_consistent_stable": None})
    out["self_consistency"] = verdicts
    (HERE / "attempt-results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(verdicts, indent=2))


if __name__ == "__main__":
    main()
