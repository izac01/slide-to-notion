# main.py (append at bottom, guarded)
if __name__ == "__main__":
    from pipeline import run_mvp
    # TODO: accept CLI args later; for MVP just run defaults
    results = run_mvp()
    print("MVP run complete. Created pages:", [r["result"].get("url") for r in results])
