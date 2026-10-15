name: YouTube Bot Auto
on:
  workflow_dispatch:

permissions:
  contents: write

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: sudo apt-get update && sudo apt-get install -y ffmpeg
      - run: pip install -r requirements.txt
      - run: ls -la
      - run: python -u bot.py
        env:
          YOUTUBE_TOKEN_JSON: ${{ secrets.YOUTUBE_TOKEN_JSON }}
