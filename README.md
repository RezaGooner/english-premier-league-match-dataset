# Comprehensive English Premier League Match Dataset (2000–2026)

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22055597-blue)](https://zenodo.org/records/22055597)
![Matches](https://img.shields.io/badge/matches-9%2C880-brightgreen)
![Seasons](https://img.shields.io/badge/seasons-26-brightgreen)
![Columns](https://img.shields.io/badge/columns-65-brightgreen)

A match-level dataset covering **26 English Premier League seasons**, from **2000/2001** through **2025/2026**, combining classic scoreline data with in-game statistics, Expected Goals (xG), end-of-season standings, managers, geography, historical club form, and head-to-head form — all in a single flat CSV, ready for machine learning and analysis.

- 📦 **GitHub:** [RezaGooner/english-premier-league-match-dataset](https://github.com/RezaGooner/english-premier-league-match-dataset)
- 📚 **Zenodo (citable, versioned):** [10.5281/zenodo.22050039](https://zenodo.org/records/22055597)

---

## Table of Contents
- [Overview](#overview)
- [Dataset at a Glance](#dataset-at-a-glance)
- [Data Dictionary](#data-dictionary)
- [Data Quality & Known Limitations](#data-quality--known-limitations)
- [Quickstart](#quickstart)
- [Example Use Cases](#example-use-cases)
- [Data Sources](#data-sources)
- [Repository Contents](#repository-contents)
- [Future Updates](#future-updates)
- [Citation](#citation)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Overview

This dataset was built by aggregating and cross-referencing publicly available football data (results, in-game stats, standings, and club/manager metadata) into a single, analysis-ready table: **one row per match**. It is intended for machine learning engineers, data scientists, and sports analysts working on match outcome prediction, performance analysis, feature engineering, and historical trend analysis of the Premier League.

## Dataset at a Glance

| | |
|---|---|
| **Rows (matches)** | 9,880 |
| **Columns (features)** | 65 |
| **Seasons covered** | 26 — `2000/01` to `2025/26` |
| **Unique clubs** | 46 |
| **Unique managers** | 157 |
| **Unique referees** | 85 |
| **Unique stadiums** | 53 |
| **Derby matches** | 834 (8.4% of all matches) |
| **Result split** | Home win 45.7% · Away win 29.5% · Draw 24.8% |
| **File format** | CSV, UTF-8 |

## Data Dictionary

### 1. Match Identification & Timeline
| Column | Description |
|---|---|
| `Season` | Season code, e.g. `0001` = 2000/01, `2425` = 2024/25 |
| `Year`, `Month`, `Day`, `WeekDay`, `Time` | Kickoff date/time details |
| `Round` | Matchweek number (1–38) |

### 2. Team & Location Metadata
| Column | Description |
|---|---|
| `HomeTeam`, `AwayTeam` | Club names |
| `HomeCity`, `HomeRegion`, `AwayCity`, `AwayRegion` | Club geography (regions: North, South, Midlands, East, West) |
| `IsDerby` | `Yes`/`No` — local/regional derby flag |
| `HomeStadium` | Venue name |
| `HomeManager`, `AwayManager` | Managers in charge at kickoff |

### 3. Match Outcomes & Results
| Column | Description |
|---|---|
| `HomeGoal`, `AwayGoal` | Full-time goals |
| `Result` | `H` / `D` / `A` |
| `HomeGoal-HalfTime`, `AwayGoal-HalfTime`, `Result-HalfTime` | Half-time score & outcome |

### 4. In-Game Statistics
| Column | Description |
|---|---|
| `Attendance` | Spectator count (`0` matches played during the COVID-19 pandemic, see [Data Quality](#data-quality--known-limitations)) |
| `Referee` | Match official |
| `HomeShot`, `AwayShot` | Total shots |
| `HomeOnTargetShot`, `AwayOnTargetShot` | Shots on target |
| `HomeFoul`, `AwayFoul` | Fouls |
| `HomeCorner`, `AwayCorner` | Corners |
| `HomeYellow`, `AwayYellow`, `HomeRed`, `AwayRed` | Disciplinary cards |
| `XGHome`, `XGAway` | Expected Goals — modern seasons only |
| `VAR` | `Yes`/`No` — Whether VAR was available for that match |

### 5. Season Context (End-of-Season Standings)
> ⚠️ **Leakage warning:** these columns describe the club's *final* table position/stats for that season, known only after the season ends. Do not use them as-is for in-season / pre-match prediction — see [Data Quality](#data-quality--known-limitations).

| Column | Description |
|---|---|
| `SeasonPosHome`, `SeasonPosAway` | Final league position |
| `SeasonPlayedHome`, `SeasonPlayedAway` | Matches played that season (typically 38) |
| `SeasonWin/Draw/Loss{Home,Away}` | Final win/draw/loss totals |
| `SeasonGF/GA/GD{Home,Away}` | Final goals for / against / difference |
| `SeasonPoints{Home,Away}` | Final points total |
| `QualificationOrRelegation{Home,Away}` | Final zone outcome (e.g. Champions League qualification, relegation) |

### 6. Historical & Form Data
| Column | Description |
|---|---|
| `HomeTrophies`, `AwayTrophies` | Historical trophy count of the club |
| `PremierLeagueHome`, `PremierLeagueAway`, `FACupHome`, `FACupAway`, `CarabaoCupHome`, `CarabaoCupAway`, `CommunityShieldHome`, `CommunityShieldAway`, `ChampionsLeagueHome`, `ChampionsLeagueAway`, `EuropaLeagueHome`, `EuropaLeagueAway`, `ConferenceLeagueHome`, `ConferenceLeagueAway`, `SuperCupHome`, `SuperCupAway`, `ClubWorldCupHome`, `ClubWorldCupAway`, `IntercontinentalCupHome`, `IntercontinentalCupAway` | The value is Yes if the team, as either the home or away side, won this trophy in this season; otherwise, No |
| `HomeForm`, `AwayForm` | Recent form string, e.g. `WWDLW` (most recent 5 results) |
| `H2HForm` | Head-to-head form between the two specific clubs |

## Data Quality & Known Limitations

This section is based on a direct profiling of the released CSV and is included so users know what to expect before modeling:

- **xG coverage is partial by design.** `XGHome`/`XGAway` are ~**71% missing** overall: xG data only exists from the 2018/19 season onward (partial that season, complete from 2019/20). Filter to modern seasons if xG is required for your analysis.
- **VAR flag reflects real-world rollout.** `VAR` is `No` for all matches before the 2019/20 season (the season the Premier League introduced VAR), partially `Yes` in 2019/20, and `Yes` for every match from 2020/21 onward.
- **`Attendance` = 0 marks fanless matches**, not missing data — this occurs for matches in the 2019/20 season played behind closed doors during the COVID-19 pandemic (363 matches).
- **Form fields have light missingness** at the start of the historical window, where insufficient prior matches exist to compute form: `H2HForm` ~8.1% missing, `HomeForm`/`AwayForm` <0.5% missing.
- **No duplicate rows** were found in the released file (checked across all 65 columns).
- **Season-context columns are end-of-season, not point-in-time** (see the leakage warning above) — for temporal/mid-season prediction tasks, compute rolling stats up to the match date instead of using these columns directly.

## Quickstart

```python
import pandas as pd

df = pd.read_csv("matches.csv", dtype={"Season": str})

print(df.shape)                     # (9880, 65)
print(df["Result"].value_counts())  # H / D / A distribution

# Example: modern-era subset with reliable xG + VAR data
modern = df[df["Year"] >= 2019]

# Example: safe feature set for pre-match prediction (drops end-of-season leakage columns)
leak_cols = [c for c in df.columns if c.startswith("Season") or c.startswith("Qualification")]
safe_df = df.drop(columns=leak_cols)
```

## Example Use Cases

1. **Predictive modeling** — classification models (Random Forest, XGBoost, neural nets) to predict `Result`, using pre-match-safe features and engineered rolling form.
2. **Time series / momentum analysis** — track a club's form, goal difference, or points trajectory across a season.
3. **Causal / historical analysis** — quantify the effect of VAR introduction, derby pressure, managerial changes, or playing behind closed doors on match outcomes.
4. **Expected Goals research** — compare xG vs. actual goals for the post-2018 subset to study finishing efficiency or model calibration.

## Data Sources

Compiled and cross-referenced from:
- [11v11](https://www.11v11.com/)
- [FBref](https://fbref.com/)
- [Sky Sports](https://www.skysports.com/)
- [Premier League official website](https://www.premierleague.com/)
- [StatMuse](https://www.statmuse.com/)
- [Transfermarkt](https://www.transfermarkt.com/)
- [ESPN](https://www.espn.com/)

## Repository Contents

| File | Description |
|---|---|
| `matches.csv` | The main dataset (9,880 × 65) |
| `Notebook1.ipynb` – `Notebook9.ipynb` | Data collection, cleaning, and EDA notebooks documenting how the dataset was built |
| `README.md` | This file |

## Future Updates

This is a **living dataset**:
- Older/historical pre-2000 seasons may be added to extend coverage further back.
- New seasons will be appended after each season concludes.

Check the [Zenodo record](https://zenodo.org/records/22050039) for versioned, citable releases, and the [GitHub repo](https://github.com/RezaGooner/english-premier-league-match-dataset) for the latest in-progress work.

## Citation

If you use this dataset in academic or analytical work, please cite it via its Zenodo DOI:

```bibtex
@dataset{asadi_epl_dataset,
  author       = {Reza Asadi},
  title        = {Comprehensive English Premier League Match Dataset (2000-2026)},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.22050039},
  url          = {https://zenodo.org/records/22050039}
}
```

## License

Published under **[Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)**. You are free to share and adapt the material for **non-commercial purposes**, provided appropriate credit is given.

## Contributing

Issues, corrections, and pull requests are welcome on [GitHub](https://github.com/RezaGooner/english-premier-league-match-dataset/issues) — especially reports of data discrepancies, since this dataset is compiled from multiple cross-referenced sources.

## Contact

**Author:** Reza Asadi (RezaGooner)
For questions or collaboration, please open an issue on the [GitHub repository](https://github.com/RezaGooner/english-premier-league-match-dataset/issues).
