import subprocess
import argparse
from datetime import datetime

def run_pipeline(screenshot_date=None):
    # If no date provided, use today's date
    if not screenshot_date:
        screenshot_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Run screenshot extraction
        print(f"Running screenshot extraction for date: {screenshot_date}")
        subprocess.run(["python", "extraction/src/main.py", "--screenshot", screenshot_date], check=True)
        
        # Count posts
        print("Counting posts...")
        subprocess.run(["python", "scripts/count_posts.py"], check=True)
        
        # Update stats in HTML
        print("Updating stats in HTML...")
        subprocess.run(["python", "scripts/update_stats_in_html.py"], check=True)
        
        print("Pipeline completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running pipeline: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the complete pipeline for processing screenshots and updating stats")
    parser.add_argument("--screenshot", help="Date for screenshot processing (YYYY-MM-DD)", required=False)
    
    args = parser.parse_args()
    run_pipeline(args.screenshot) 