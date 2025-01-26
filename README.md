# Commands

## Running web server
```
hugo server
```

## Running script to update stats
```
source venv/bin/activate
python extraction/src/main.py --screenshot 2024-12-04
python scripts/count_posts.py
python scripts/update_stats_in_html.py

Or just
python scripts/run_pipeline.py --screenshot 2024-12-04
```
