# src/main.py

import os
import argparse
from ocr_extractor import OCRExtractor

def main(screenshot):
    # Example screenshot path
    # screenshot_path = os.path.join('screenshots', 'fitbitshare_506576545.png')
    screenshot_path = os.path.join('extraction', 'screenshots', screenshot+'.jpg')

    # Initialize OCR extractor (True to use EasyOCR, False for Tesseract)
    use_easyocr = False  # Change to True to use EasyOCR
    ocr_extractor = OCRExtractor(use_easyocr)

    # coordinates = [
    #     (53, 1211, 269, 75),
    #     (566, 1479, 111, 43),
    #     (51, 1681, 144, 44),
    # ]
    # results = ocr_extractor.extract_text_from_coordinates(screenshot_path, coordinates)

    # Extract text and print results
    results = ocr_extractor.extract_text(screenshot_path)
    for result in results:
        print(f"Text: '{result['text']}' at position: {result['position']}")

    # Create markdown file
    md_filename = f"content/posts/{screenshot}.md"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(md_filename), exist_ok=True)
    
    # Create markdown content
    md_content = f"""
+++
title = 'Hello'
date = {screenshot}
draft = false
+++
## Map

![img](/trailblazer/runs/{screenshot}.jpeg)

## Stats

### Distance (km)
{results[0]['text']}

### Heart Rate (bpm)
{results[1]['text']}

### Pace (min/km)
{results[2]['text']}

### Time
{results[3]['text']}

## Notes
N/A
"""

    # Write to file
    with open(md_filename, 'w') as f:
        f.write(md_content)
    
    input_file = f"extraction/screenshots/{screenshot}.jpg"
    output_file = f"static/runs/{screenshot}.jpeg"
    ocr_extractor.extract_map_region(input_file, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="OCR Text Extraction")
    parser.add_argument(
        '--screenshot',
        required=True,
        help="Path to the screenshot image."
    )
    args = parser.parse_args()
    main(args.screenshot)
