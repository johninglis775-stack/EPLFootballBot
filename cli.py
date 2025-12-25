import argparse

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, help="Output directory path")
    p.add_argument("--token", required=True, help="football-data API token")
    return p.parse_args()
