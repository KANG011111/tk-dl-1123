"""Prepare local environment for shorts-download1121."""

from __future__ import annotations

from pathlib import Path

REQUIRED_DIRS = [
    Path("downloads"),
    Path("assets/samples"),
    Path("tests/fixtures"),
]


def main() -> None:
    for path in REQUIRED_DIRS:
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ ensured {path}")
    env_example = Path(".env.example")
    if not env_example.exists():
        env_example.write_text(
            "# Copy to .env and adjust paths if needed\nSHORTS_DL_DOWNLOADS_DIR=downloads\n",
            encoding="utf-8",
        )
        print("📄 created .env.example")


if __name__ == "__main__":
    main()
