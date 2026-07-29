# stats-dashboard

Live-дашборд метрик соцсетей Maria. Автосбор через ScrapeCreators + GitHub Actions cron, статический сайт на GitHub Pages.

## Что внутри

- `accounts.yml` — список отслеживаемых аккаунтов (6 канонических на 2026-07-20)
- `scripts/fetch/` — Python-скрипты по платформам, дёргают ScrapeCreators API
- `data/{platform}/{handle}/{YYYY-MM-DD}.json` — daily снапшоты
- `site/` — статический сайт (vanilla HTML + Chart.js), деплой на GH Pages
- `.github/workflows/fetch-daily.yml` — cron 08:00 UTC → fetch → commit → сайт rebuilds
- `.github/workflows/deploy-pages.yml` — build site и publish

## Локальный запуск

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export SCRAPECREATORS_API_KEY=...
python scripts/fetch/fetch_instagram.py marketplacecard
```

## GitHub secrets

Один ключ `SCRAPECREATORS_API_KEY` в GitHub Actions Secrets — один для всех платформ. Пример env-файла — `config/scrapecreators-key.env.example`.

## Метрики

Для каждого аккаунта: followers, growth day/week/month, total posts, last 20 posts (likes/comments/shares/saves/views/plays), top posts by engagement, cadence.

## Season

Season 2026-2027. Private repo, owner mborodkina2621987-tech.
