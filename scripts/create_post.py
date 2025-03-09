import os
from PIL import Image

def create_post(date, distance, heart_rate, pace, time, title):
    title = title.replace('_', ' ')

    # Create markdown file
    md_filename = f"content/posts/{date}.md"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(md_filename), exist_ok=True)
    
    # Create markdown content
    md_content = f"""
+++
title = '{title}'
date = {date}
draft = false
+++
## Map

![img](/trailblazer/runs/{date}.jpeg)

## Stats

### Distance (km)
{distance}

### Heart Rate (bpm)
{heart_rate}

### Pace (min/km)
{pace}

### Time
{time}

## Notes
N/A
"""

    # Write to file
    with open(md_filename, 'w') as f:
        f.write(md_content)
    
    input_file = f"extraction/screenshots/{date}.jpg"
    output_file = f"static/runs/{date}.jpeg"

    # Save copy of image over because legacy
    img = Image.open(input_file)
    img.save(output_file)

    print(f"Created post for {date}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Read run stats from data.csv')
    parser.add_argument('date', type=str, help='Date string in YYYY-MM-DD format')
    parser.add_argument('distance', type=str, help='Distance in miles')
    parser.add_argument('heart_rate', type=str, help='Average heart rate')
    parser.add_argument('pace', type=str, help='Average pace per mile')
    parser.add_argument('time', type=str, help='Total time')
    parser.add_argument('title', type=str, help='Title of post')
    
    args = parser.parse_args()
    create_post(args.date, args.distance, args.heart_rate, args.pace, args.time, args.title)
