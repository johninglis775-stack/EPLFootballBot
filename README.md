# EPLFootballBot
# EPL FootballBot

**Version:** 1.0  
**Status:** Spec locked – implementation in progress

EPL FootballBot is a **pure data-collection tool** for English Premier League football.

It is **not** a prediction system, **not** a betting system, and **not** an analysis engine.

Its only job is to:
- Collect **honest, pre-match EPL fixture data**
- Structure it into a stable, machine-readable format
- Explicitly report when data is missing or unavailable

All reasoning, modelling, betting logic, and interpretation happens **outside** FootballBot.

---

## Core Philosophy

- FootballBot is a **data sensor, not a brain**
- **NO_DATA is a valid outcome**, not an error
- Partial data is expected and must be reported honestly
- The bot must **never invent fixtures, odds, or context**
- Missing data is left **blank**, never guessed
- Stability and transparency matter more than completeness

---

## Data Sources

### Fixtures & Context (Source of Truth)
- **football-data API**
  - EPL fixtures
  - Gameweek / round
  - Kickoff dates & times (UTC)
  - Team names and IDs
  - League standings (TOTAL / HOME / AWAY)
  - Match history (for last-5 aggregates)

If football-data does not list a fixture, FootballBot will not create it.

---

### Odds & Markets (Enrichment Only)
- **Sportbex (Soccer odds endpoints)**
  - 1X2
  - Over/Under 2.5
  - BTTS
  - Asian lines (optional, v2)

Odds never define fixtures.  
They are attached **only** to fixtures already confirmed by football-data.

---

## Outputs (Every Run)

FootballBot always produces **three files**, even on NO_DATA days:

1. **`epl_fixtures.csv`**
   - One row per EPL fixture
   - Stable column order
   - Blank fields allowed where data is missing

2. **`coverage.json`**
   - Machine-readable diagnostics
   - Expected vs fetched fixtures
   - Missing odds counts
   - Status: `OK`, `PARTIAL`, `NO_DATA`, or `FAILED`

3. **`notes.txt`**
   - Human-readable explanation of what happened
   - Clear reasons for missing data or NO_DATA

---

## Status Semantics

| Condition | Status |
|--------|--------|
| No scheduled EPL fixtures | NO_DATA |
| Fixtures exist, all required data present | OK |
| Fixtures exist, some data missing | PARTIAL |
| Cannot determine fixtures at all | FAILED |

Fixtures existing always beats odds completeness.

---

## Data Contract

Every field in `epl_fixtures.csv` is explicitly classified as:

- **RAW** – copied directly from football-data or Sportbex
- **DERIVED** – mechanical calculation only (dates, sums, counts)

No field contains predictions, ratings, or opinion.

The full field-level schema is defined in:
- `docs/field_level_data_spec.md`

Column order is stable.  
New columns may only be appended in v1.x releases.

---

## Implementation Plan (v1.0)

Development is incremental and safe:

1. Fixtures discovery & NO_DATA handling
2. League standings snapshot
3. Last-5 form & scheduling context
4. Sportbex odds (1X2)
5. Over/Under 2.5 + BTTS
6. Hardening for daily runs

At the end of every step, FootballBot remains runnable and honest.

---

## What FootballBot Does NOT Do

- No predictions
- No betting strategies
- No team strength modelling
- No filtering or ranking
- No decision-making
- No automation of bets

FootballBot provides **data only**.

---

## Versioning Policy

- **v1.0** – initial locked schema
- **v1.x** – additive, backward-compatible changes only
- **v2.0** – breaking schema changes

CSV stability is non-negotiable.

---

## License & Usage

Internal / experimental use.

This project prioritises correctness, transparency, and auditability over speed or cleverness.

