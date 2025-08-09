from pipeline import run

def main(auth: str, database_id: str) -> None:
    run(auth, database_id)

if __name__ == "__main__":
    main("fake_auth", "fake_db_id")
