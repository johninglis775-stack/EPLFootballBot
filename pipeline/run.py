from datetime import datetime, timezone
from dateutil import parser
from pathlib import Path
from providers.fixtures_football_data import get_scheduled_fixtures
from schemas.csv_schema import CSV_HEADERS
from schemas.coverage_schema import empty_coverage
from outputs.writers import write_csv, write_json, write_notes
from outputs.raw_store import save_raw
from dateutil import tz
UK_TZ = tz.gettz("Europe/London")
def run(out_dir, token):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    coverage = empty_coverage()
    now_utc = datetime.now(timezone.utc).isoformat()
    coverage["run_date_utc"] = now_utc

    rows = []

    try:
        data = get_scheduled_fixtures(token)
        save_raw(out_dir, "fixtures_scheduled.json", data)
    except Exception as e:
        coverage["status"] = "FAILED"
        coverage["status_reason"] = f"Error fetching fixtures: {e}"
        write_csv(f"{out_dir}/epl_fixtures.csv", CSV_HEADERS, [])
        write_json(f"{out_dir}/coverage.json", coverage)
        write_notes(f"{out_dir}/notes.txt", [
            f"Date (UTC): {now_utc}",
            "Status: FAILED",
            coverage["status_reason"]
        ])
        return

    matches = data.get("matches", [])

    if not matches:
        coverage["status"] = "NO_DATA"
        coverage["status_reason"] = "No scheduled EPL fixtures returned by football-data."
        write_csv(f"{out_dir}/epl_fixtures.csv", CSV_HEADERS, [])
        write_json(f"{out_dir}/coverage.json", coverage)
        write_notes(f"{out_dir}/notes.txt", [
            f"Date (UTC): {now_utc}",
            "Status: NO_DATA",
            coverage["status_reason"]
        ])
        return

    gameweeks = [m.get("matchday") for m in matches if m.get("matchday") is not None]
    target_gw = min(gameweeks)
    target_matches = [m for m in matches if m.get("matchday") == target_gw]

    coverage["gameweek"] = target_gw
    coverage["expected_fixtures"] = len(target_matches)

    # Try to read season label from API response (fallback to None if absent)
    season_label = None
    try:
        comp = data.get("competition", {})
        season = comp.get("season", {})
        start_y = (season.get("startDate") or "")[:4]
        end_y = (season.get("endDate") or "")[:4]
        if start_y and end_y:
            season_label = f"{start_y}-{end_y}"
    except Exception:
        season_label = None

    for m in target_matches:
        kickoff = parser.isoparse(m["utcDate"])
        rows.append({
            "Season": season_label or "",
            "Competition": (data.get("competition", {}) or {}).get("name", "") or "",
            "GameWeek": target_gw,
            "FixtureId": m.get("id", ""),
            "OddsFetchTimestampUTC": now_utc,
            "MatchDate": kickoff.date().isoformat(),
            "KickoffTimeUTC": kickoff.time().strftime("%H:%M"),
            "KickoffDateTimeUTC": kickoff.isoformat(),
            "KickoffTimeLocal": kickoff.astimezone(UK_TZ).time().strftime("%H:%M"),

            "HomeTeam": (m.get("homeTeam", {}) or {}).get("name", "") or "",
            "AwayTeam": (m.get("awayTeam", {}) or {}).get("name", "") or "",
            "HomeTeamId": (m.get("homeTeam", {}) or {}).get("id", "") or "",
            "AwayTeamId": (m.get("awayTeam", {}) or {}).get("id", "") or "",
        })

    coverage["fetched_fixtures"] = len(rows)
    coverage["status"] = "SUCCESS"
    coverage["status_reason"] = "Fixtures fetched successfully."

    write_csv(f"{out_dir}/epl_fixtures.csv", CSV_HEADERS, rows)
    write_json(f"{out_dir}/coverage.json", coverage)
    write_notes(f"{out_dir}/notes.txt", [
        f"Date (UTC): {now_utc}",
        f"Season: {season_label or 'unknown'}",
        f"Gameweek: {target_gw}",
        f"Fixtures expected: {coverage['expected_fixtures']}",
        f"Fixtures fetched: {coverage['fetched_fixtures']}",
        "Status: SUCCESS"
    ])
