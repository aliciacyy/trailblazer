import os
import json
from datetime import datetime

def count_posts():
    posts_dir = "content/posts"
    stats_file = "data/stats.json"
    
    # Count all markdown files in posts directory and its subdirectories
    post_count = 0
    # Initialize total distance
    total_distance = 0
    

    for root, dirs, files in os.walk(posts_dir):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                post_count += 1
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Find the distance line
                        distance_lines = [line.strip() for line in content.split('\n') 
                                       if '### Distance (km)' in line]
                        if distance_lines:
                            # Get the next line after "Distance (km)"
                            distance_idx = content.split('\n').index(distance_lines[0])
                            if distance_idx + 1 < len(content.split('\n')):
                                distance_value = content.split('\n')[distance_idx + 1].strip()
                                # Clean and convert the distance value
                                try:
                                    # Remove any trailing colon and convert to float
                                    distance_value = distance_value.rstrip(':')
                                    distance = float(distance_value)
                                    total_distance += distance
                                except ValueError:
                                    # Skip if value cannot be converted to float
                                    continue
                except (IOError, UnicodeDecodeError):
                    continue
    
    # Prepare stats data
    stats = {
        "total_posts": post_count,
        "total_distance": round(total_distance, 2),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(stats_file), exist_ok=True)
    
    # Write to stats.json
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4)

if __name__ == "__main__":
    count_posts() 