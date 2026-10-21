# Douze Points for the Neighbours

Interactive analysis of geographical voting favoritism in Eurovision (1957–2023).
Everything is computed in Python; GitHub builds the page and publishes it with GitHub Pages on every push.

## Run locally

    pip install -r requirements.txt
    python build.py

Then open `site/index.html` in a browser.

## Put it online (GitHub Pages)

1. Create a new **public** repository on github.com (e.g. `eurovision-favoritism`).
2. Upload every file in this folder, including the hidden `.github` folder
   (drag the folder into "uploading an existing file", or `git push`).
3. In the repository: **Settings → Pages → Source: GitHub Actions**.
4. Open the **Actions** tab and wait for "Build and deploy site" to turn green.
   The site is at `https://<your-username>.github.io/<repository-name>/`.

Every later push rebuilds the site automatically.

## Files

- `analysis.py` – the calculations: normalised favoritism per directed pair per show, leave-one-out baseline,
  separate jury/televote favoritism from 2016, cluster definitions (`CLUSTER_SCHEMES`).
  `python analysis.py` prints the Nordic matrix and the strongest pairs.
- `build.py` – runs the analysis and writes the data into `site/index.html`.
- `template.html` – layout and the five views (Plotly).
- `votes.csv` – the dataset.
- `world_50m.json` – map outlines (Natural Earth 1:50m), embedded so the map needs no extra downloads.
- `.github/workflows/deploy.yml` – builds and publishes the site on GitHub.

## Favoritism

    share      = points A gave B / all points A gave in that show
    favoritism = (share − B's average share from all other voters in that show) × 58

Since 2016 every country gives two sets of 1–8, 10, 12 (jury + televote, 116 points, up to 24 to one country).
Working with shares and expressing the result on one 58-point set keeps the years comparable.
