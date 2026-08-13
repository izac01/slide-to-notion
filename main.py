# main.py
import argparse
from typing import Sequence

from pipeline import run_mvp


def main(argv: Sequence[str] | None = None) -> list[dict]:
    parser = argparse.ArgumentParser(description="Convert Google Slides into Notion pages.")
    parser.add_argument("--slides", default="workspace/slides.json", help="path to the slides JSON")
    parser.add_argument("--database-id", default=None, help="Notion database id (falls back to NOTION_DATABASE_ID)")
    parser.add_argument("--limit", type=int, default=3, help="how many slides to convert")
    args = parser.parse_args(argv)

    results = run_mvp(
        slides_path=args.slides,
        pick=range(args.limit),
        database_id=args.database_id,
    )
    print("MVP run complete. Created pages:", [r["result"].get("url") for r in results])
    return results


if __name__ == "__main__":
    main()
