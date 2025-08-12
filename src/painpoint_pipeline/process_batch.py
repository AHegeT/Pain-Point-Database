# process_batch.py

import os
import csv
import uuid
import logging
import configparser
from datetime import datetime
from dataclasses import dataclass, asdict
import pytesseract
from PIL import Image

# --- DATA STRUCTURE ---
@dataclass
class PainPoint:
    """A class to hold structured data for a single pain point."""
    pain_point_id: str
    date_observed: str
    source_platform: str
    raw_text: str
    screenshot_link: str
    primary_quote: str = ""
    author_handle: str = ""
    engagement_score: int = 0
    supporting_quotes: str = ""
    my_solution_idea: str = ""

# --- UTILITY FUNCTIONS ---

def get_text_from_image(image_path):
    """Performs OCR on a single image and returns the extracted text."""
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def append_to_csv(data_row: PainPoint, db_file: str):
    """Appends a PainPoint dataclass instance as a new row to a CSV file."""
    row_dict = asdict(data_row)
    headers = list(row_dict.keys())
    
    if not os.path.exists(db_file):
        with open(db_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    
    with open(db_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(row_dict)

def archive_file(source_path, archive_dir):
    """Moves a file to the archive directory."""
    filename = os.path.basename(source_path)
    destination_path = os.path.join(archive_dir, filename)
    os.rename(source_path, destination_path)
    return filename

# --- MAIN WORKFLOW FUNCTION ---

def process_image(image_path, db_file, archive_dir):
    """Main workflow to process a single image."""
    try:
        raw_text = get_text_from_image(image_path).strip()
        mod_time = os.path.getmtime(image_path)
        
        # Instantiate the dataclass with the extracted data
        new_entry = PainPoint(
            pain_point_id=str(uuid.uuid4()),
            date_observed=datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d'),
            source_platform='Discord',
            raw_text=raw_text,
            screenshot_link=os.path.basename(image_path)
        )
        
        append_to_csv(new_entry, db_file)
        logging.info(f"✅ Processed and saved data for {new_entry.screenshot_link}")
        
        archived_filename = archive_file(image_path, archive_dir)
        logging.info(f"🗄️ Archived: {archived_filename}")

    except Exception as e:
        logging.error(f"❌ Failed to process {os.path.basename(image_path)}: {e}", exc_info=True)

# --- SCRIPT EXECUTION ---

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    DB_FILE = config['Paths']['database_file']
    PROCESS_FOLDER = config['Paths']['process_folder']
    ARCHIVE_FOLDER = config['Paths']['archive_folder']
    LOG_FILE = config['Logging']['log_file']

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
    )

    os.makedirs(PROCESS_FOLDER, exist_ok=True)
    os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

    logging.info("--- Starting Batch Process ---")
    image_files = [f for f in os.listdir(PROCESS_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        logging.info(f"No images found in '{PROCESS_FOLDER}'.")
    else:
        logging.info(f"Found {len(image_files)} images to process...")
        for filename in image_files:
            full_path = os.path.join(PROCESS_FOLDER, filename)
            process_image(full_path, DB_FILE, ARCHIVE_FOLDER)
        logging.info("--- 🎉 Batch Processing Complete ---")