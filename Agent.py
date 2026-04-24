name: Daily AI News Agent

on:
  schedule:
    - cron: "30 1 * * *"
  workflow_dispatch:

jobs:
  run-agent:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run AI News Agent
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: python Agent.py
