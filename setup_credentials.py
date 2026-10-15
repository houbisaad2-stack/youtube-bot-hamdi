name: YouTube Bot Auto
on:
  workflow_dispatch:
  schedule:
    - cron: '0 10 * * *'
jobs:
  upload:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - name: Install ffmpeg
        run: sudo apt-get update && sudo apt-get install -y ffmpeg
      - name: Install deps
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run bot
        env:
          YOUTUBE_TOKEN_JSON: ${{ secrets.YOUTUBE_TOKEN_JSON }}
        run: python bot.py
      - name: Save log
        run: |
          git config user.name "bot"
          git config user.email "bot@github.com"
          git add uploaded.json || true
          git diff --quiet && git diff --staged --quiet || (git commit -m "uploaded log [skip ci]" && git push)
