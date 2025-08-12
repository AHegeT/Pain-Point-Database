import sys
import os
import csv
import uuid
from datetime import datetime
import pytesseract
from PIL import Image

# --- CONFIGURATION ---
DATABASE_FILE = 'pain_points.csv'
PROCESS_FOLDER = 'To_Process'   # Folder to get images from
ARCHIVE_FOLDER = 'Archived'     # Folder to move processed images to

def ensure_header_exists(db_file, headers):
    """Checks if the CSV file exists and has a header. If not, it creates it."""
    if not os.path.exists(db_file):
        with open(db_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def extract_and_save(image_path, db_file):
    """
    Performs OCR on an image, saves the data to a CSV,
    and then archives the image file.
    """
    try:
        # 1. Perform OCR
        img = Image.open(image_path)
        raw_text = pytesseract.image_to_string(img)
        
        # 2. Generate data for the new row
        unique_id = str(uuid.uuid4())
        mod_time = os.path.getmtime(image_path)
        date_observed = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
        source_platform = 'Discord'
        
        # 3. Prepare the row
        new_row = {
            'Pain_Point_ID': unique_id, 'Date_Observed': date_observed,
            'Source_Platform': source_platform, 'Primary_Quote': '',
            'Author_Handle': '', 'Engagement_Score': '',
            'Supporting_Quotes': '', 'My_Solution_Idea': '',
            'Raw_Text': raw_text.strip(),
            'Screenshot_Link': os.path.basename(image_path)
        }
        
        # 4. Append the new row to the CSV
        headers = list(new_row.keys())
        ensure_header_exists(db_file, headers)
        
        with open(db_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerow(new_row)
            
        print(f"✅ Processed: {os.path.basename(image_path)}")

        # 5. Move the processed file to the archive folder
        filename = os.path.basename(image_path)
        destination_path = os.path.join(ARCHIVE_FOLDER, filename)
        os.rename(image_path, destination_path)
        
    except Exception as e:
        print(f"❌ ERROR processing {os.path.basename(image_path)}: {e}")

# --- RUN THE SCRIPT ---
if __name__ == "__main__":
    # Create necessary folders if they don't exist
    os.makedirs(PROCESS_FOLDER, exist_ok=True)
    os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
    
    # Get a list of all files in the processing folder
    try:
        image_files = [f for f in os.listdir(PROCESS_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except FileNotFoundError:
        print(f"Error: The directory '{PROCESS_FOLDER}' was not found.")
        sys.exit(1)

    if not image_files:
        print(f"No images found in '{PROCESS_FOLDER}'.")
    else:
        print(f"Found {len(image_files)} images to process...")
        # Loop through each image file and process it
        for filename in image_files:
            full_path = os.path.join(PROCESS_FOLDER, filename)
            extract_and_save(full_path, DATABASE_FILE)
        print("🎉 Batch processing complete!")