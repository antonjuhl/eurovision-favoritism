"""
Builds site/index.html — one self-contained, interactive page.

    python build.py            (expects votes.csv in the same folder)

On GitHub, .github/workflows/deploy.yml runs this on every push and publishes site/ with GitHub Pages.

All the analysis (normalisation, leave-one-out baseline, jury/televote split)
happens here in Python, see analysis.py. The page receives one row per
voter -> recipient per show and only averages those rows live, so the
filters (period, finals/semis, minimum shared years, cluster scheme) respond
instantly without a server.
"""
import json
from pathlib import Path

import numpy as np

from analysis import CLUSTER_SCHEMES, COORDS, ISO3, NAMES, build_table

HERE = Path(__file__).parent


def payload() -> dict:
    t = build_table(HERE / "votes.csv")
    ids = sorted(set(t.from_country_id) | set(t.to_country_id))
    idx = {c: i for i, c in enumerate(ids)}

    def col(s, scale=100):
        return [None if np.isnan(v) else int(round(v * scale)) for v in s]

    return {
        "countries": [
            {"id": c, "name": NAMES.get(c, c.upper()), "iso3": ISO3.get(c),
             "lat": COORDS.get(c, (None, None))[0], "lon": COORDS.get(c, (None, None))[1]}
            for c in ids
        ],
        "schemes": CLUSTER_SCHEMES,
        "rows": {
            "y": t.year.astype(int).tolist(),
            "s": (t.stage == "S").astype(int).tolist(),   # 0 = final, 1 = semi-final
            "f": [idx[c] for c in t.from_country_id],
            "t": [idx[c] for c in t.to_country_id],
            "ex": col(t.ex),        # favoritism x100
            "te": col(t.tele),      # televote-only favoritism x100 (2016+)
            "ju": col(t.jury),      # jury-only favoritism x100 (2016+)
        },
        "years": [int(t.year.min()), int(t.year.max())],
    }


def main():
    data = json.dumps(payload(), separators=(",", ":"))
    html = (HERE / "template.html").read_text(encoding="utf-8").replace("/*__DATA__*/null", data)
    topo = (HERE / "world_50m.json").read_text(encoding="utf-8")   # map outlines, inlined
    html = html.replace("/*__TOPO__*/null", topo)
    out = HERE / "site" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
