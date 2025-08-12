# Real Estate Pain Point OCR Pipeline

This project contains a Python script that automates the process of extracting text from screenshots of online conversations to identify pain points for market research.

## Features
- **Batch Processing:** Processes all images in a specified folder (`To_Process`).
- **OCR Text Extraction:** Uses Tesseract to extract raw text from images.
- **Data Structuring:** Saves extracted data to a CSV database (`pain_points.csv`) with a unique ID and timestamp.
- **File Archiving:** Automatically moves processed images to an `Archived` folder.

## Setup

### 1. Prerequisites
- Python 3.8+
- Tesseract OCR Engine. On macOS, install with Homebrew:
```bash
  brew install tesseract
```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

Install the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Usage

1.  **Place Images:** Add your screenshot files (e.g., `.png`, `.jpg`) into the `To_Process` folder.
2.  **Run the Script:** Execute the main script from your terminal. It requires no arguments.
```bash
python process_batch.py
```

## Output

  - **`pain_points.csv`:** A CSV file where each row represents a processed screenshot. The script automatically populates the ID, date, source, and raw text. Other fields must be filled in manually.
  - **`Archived/`:** A folder containing all the screenshots that have been successfully processed.
