import json
import re

def update_total_runs():
    # Read the stats.json file
    try:
        with open('data/stats.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)
            total_posts = stats['total_posts']
            total_distance = stats['total_distance']
            total_time = stats['total_time']
            hours = total_time['hours']
            minutes = total_time['minutes']
            seconds = total_time['seconds']
    except FileNotFoundError:
        print("Error: stats.json not found")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in stats.json")
        return

    # Read the home_info.html file
    html_path = 'layouts/partials/home_info.html'
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the data-target attribute for total-runs
        pattern = r'(<p class="stat-box-no-decimal" id="total-runs" data-target=")[^"]*(")'
        updated_content = re.sub(pattern, f'\\g<1>{total_posts}\\2', content)

        pattern = r'(<span class="stat-number" id="total-distance" data-target=")[^"]*(")'
        updated_content = re.sub(pattern, f'\\g<1>{total_distance}\\2', updated_content)

        pattern = r'(<span class="stat-box-no-decimal" id="hours" data-target=")[^"]*(")'
        updated_content = re.sub(pattern, f'\\g<1>{hours}\\2', updated_content)

        pattern = r'(<span class="stat-box-no-decimal" id="minutes" data-target=")[^"]*(")'
        updated_content = re.sub(pattern, f'\\g<1>{minutes}\\2', updated_content)

        pattern = r'(<span class="stat-box-no-decimal" id="seconds" data-target=")[^"]*(")'
        updated_content = re.sub(pattern, f'\\g<1>{seconds}\\2', updated_content)

        # Write the updated content back to the file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"Successfully updated total-runs to {total_posts}")

    except FileNotFoundError:
        print(f"Error: {html_path} not found")
    except Exception as e:
        print(f"Error updating HTML: {str(e)}")


if __name__ == "__main__":
    update_total_runs() 