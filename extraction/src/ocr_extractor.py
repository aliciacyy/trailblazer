# src/ocr_extractor.py

import pytesseract
from PIL import Image
import cv2
import easyocr

class OCRExtractor:
    def __init__(self, use_easyocr=False):
        """
        Initialize OCR extractor. Use Tesseract by default or EasyOCR if specified.
        """
        self.use_easyocr = use_easyocr
        if self.use_easyocr:
            self.reader = easyocr.Reader(['en'])

    def is_within_tolerance(coord, expected_coord, tolerance=10):
        """
        Check if a coordinate is within a tolerance range of the expected coordinate.

        Args:
            coord (tuple): Actual coordinates (x1, y1, x2, y2).
            expected_coord (tuple): Expected coordinates (x1, y1, x2, y2).
            tolerance (int): Tolerance range in pixels.

        Returns:
            bool: True if coord is within tolerance range, False otherwise.
        """
        x, y, w, h = coord
        ex1, ey1, ex2, ey2 = expected_coord

        return (
            abs(x - ex1) <= tolerance and
            abs(y - ey1) <= tolerance and
            abs(w - ex2) <= tolerance and
            abs(h - ey2) <= tolerance
        )

    def extract_text_from_coordinates(self, image_path, coordinates):
        """
        Extract text from specific coordinates in an image using Tesseract.
        
        Args:
            image_path (str): Path to the image file.
            coordinates (list of tuples): List of coordinates in (x, y, w, h) format.
        
        Returns:
            list of dict: Extracted text and coordinates.
        """
        tolerance = 10
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        results = []

        for coord in coordinates:
            x, y, w, h = coord
            
            # Calculate x2, y2 for cropping
            x1, y1, x2, y2 = x, y, x + w, y + h

            # Crop the region from the grayscale image
            cropped_image = gray[y1:y2, x1:x2]

            # cv2.imwrite(f"debug_crop_{x}_{y}.png", cropped_image)

            # Perform OCR on the cropped region
            text = pytesseract.image_to_string(cropped_image, lang='eng').strip()

            # Append results
            results.append({"text": text, "position": (x, y, w, h)})

        return results


    def extract_text_with_tesseract(self, image_path):
        """Extract text and positions using Tesseract."""
        expected_coords = [
            (53, 1211, 269, 75), # distance
            (53, 1479, 95, 44), # heart rate
            (566, 1479, 111, 43), # pace
            (53, 1681, 144, 44) # time
        ]
        expected_coords_dec = [
            (53, 1377, 269, 75), # distance
            (53, 1645, 95, 44), # heart rate
            (566, 1645, 111, 43), # pace
            (51, 1847, 144, 44), # time
        ]
        expected_coords_dec_fat = [
            (51, 1478, 50, 73), # distance
            (53, 1745, 85, 44), # heart rate
            (566, 1745, 111, 44), # pace
            (53, 1943, 146, 64), # time
        ]
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # print(pytesseract.image_to_boxes(Image.open(image_path)))

        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        results = []
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                text = data['text'][i]
                x1 = data['left'][i]
                y1 = data['top'][i]
                x2 = x1 + data['width'][i]
                y2 = y1 + data['height'][i]
                coord = (x, y, w, h)
                # print(text)
                # print(coord)

                # Check if the coordinate matches any expected coordinate with tolerance
                for expected in expected_coords:
                    ex, ey, ew, eh = expected
                    if (
                        abs(x - ex) <= 5 and
                        abs(y - ey) <= 100 and
                        abs(w - ew) <= 100 and
                        abs(h - eh) <= 5
                    ):
                        results.append({"text": text, "position": coord})
                    # if self.is_within_tolerance(coord, expected_coord):
                    #     results.append({"text": text, "position": coord})
                # results.append({"text": text, "position": (x, y, w, h)})
        return results

    def extract_text_with_easyocr(self, image_path):
        """Extract text and positions using EasyOCR."""
        result = self.reader.readtext(image_path)
        results = []
        for (bbox, text, confidence) in result:
            results.append({"text": text, "position": bbox, "confidence": confidence})
        return results

    def extract_text(self, image_path):
        """General method to extract text based on selected OCR engine."""
        if self.use_easyocr:
            return self.extract_text_with_easyocr(image_path)
        else:
            return self.extract_text_with_tesseract(image_path)

    def extract_map_region(self, input_path, output_path):
        # Open the image
        img = Image.open(input_path)
        img.save(output_path)
        
        # Define the region to crop (you'll need to adjust these coordinates)
        # Format: (left, top, right, bottom)
        # map_region = (0, 0, img.width, img.height // 3)  # Approximate - adjust as needed
        
        # # Crop the image
        # map_image = img.crop(map_region)
        
        # # Save the cropped image
        # map_image.save(output_path)   
