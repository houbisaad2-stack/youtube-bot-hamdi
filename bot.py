name: YouTube Bot Auto
on:
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg
          pip install google-api-python-client google-auth google-auth-oauthlib Pillow
      - name: Credentials
        run: |
          echo '${{ secrets.YOUTUBE_CLIENT_JSON }}' > client.json
          echo '${{ secrets.YOUTUBE_TOKEN_JSON }}' > token.json
      - name: Generate
        run: python bot.py
        env:
          YOUTUBE_CLIENT_JSON: ${{ secrets.YOUTUBE_CLIENT_JSON }}
          YOUTUBE_TOKEN_JSON: ${{ secrets.YOUTUBE_TOKEN_JSON }}
