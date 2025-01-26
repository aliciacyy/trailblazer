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
    # Initialize total seconds
    total_seconds = 0
    

    for root, dirs, files in os.walk(posts_dir):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                post_count += 1
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        content_lines = content.split('\n')
                        
                        # Find the distance line
                        distance_lines = [line.strip() for line in content_lines 
                                       if '### Distance (km)' in line]
                        if distance_lines:
                            # Get the next line after "Distance (km)"
                            distance_idx = content_lines.index(distance_lines[0])
                            if distance_idx + 1 < len(content_lines):
                                distance_value = content_lines[distance_idx + 1].strip()
                                # Clean and convert the distance value
                                try:
                                    distance_value = distance_value.rstrip(':')
                                    distance = float(distance_value)
                                    total_distance += distance
                                except ValueError:
                                    continue
                        
                        # Find the time line
                        time_lines = [line.strip() for line in content_lines 
                                    if '### Time' in line]
                        if time_lines:
                            # Get the next line after "Time"
                            time_idx = content_lines.index(time_lines[0])
                            if time_idx + 1 < len(content_lines):
                                time_value = content_lines[time_idx + 1].strip()
                                # Clean and convert the time value
                                try:
                                    time_value = time_value.rstrip(':')
                                    minutes, seconds = map(int, time_value.split(':'))
                                    total_seconds += (minutes * 60 + seconds)
                                except ValueError:
                                    continue
                except (IOError, UnicodeDecodeError):
                    continue
    
    # Convert total seconds to hours, minutes, seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    # Prepare stats data
    stats = {
        "total_posts": post_count,
        "total_distance": round(total_distance, 2),
        "total_time": {
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "total_seconds": total_seconds
        },
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(stats_file), exist_ok=True)
    
    # Write to stats.json
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4)

if __name__ == "__main__":
    count_posts() 