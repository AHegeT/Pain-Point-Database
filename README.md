# Real Estate Pain Point OCR Pipeline

This project contains a Python script that automates the process of extracting text from screenshots of online conversations to identify pain points for market research.

## Features
- **Batch Processing:** Processes all images in a specified folder.
- **Configuration Driven:** Easily change folder paths and settings in a `config.ini` file.
- **OCR Text Extraction:** Uses Tesseract to extract raw text from images.
- **Data Structuring:** Saves extracted data to a CSV database with a unique ID and timestamp.
- **File Archiving:** Automatically moves processed images to an `Archived` folder.
- **Logging:** Records all operations and errors to a log file for easy debugging.
- **Tested:** Includes a test suite using `pytest` to ensure core functionality.

## Setup

### 1. Prerequisites
- Python 3.8+
- Tesseract OCR Engine. On macOS, install with Homebrew:
```bash
  brew install tesseract
```

### 2\. Create a Virtual Environment

It is highly recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install the Project

This project uses a `pyproject.toml` file for installation. Run the following command in the project's root directory to install the project in "editable" mode and all its dependencies.

```bash
pip install -e .
```

## Configuration

Before running the script for the first time, create a `config.ini` file in the root directory with the following content. You can adjust the folder and file names as needed.

```ini
[Paths]
database_file = pain_points.csv
process_folder = To_Process
archive_folder = Archived

[Logging]
log_file = ocr_pipeline.log
```

## Usage

1. **Place Images:** Add your screenshot files (e.g., `.png`, `.jpg`) into the `To_Process` folder.
2. **Run the Script:** Because the project is installed as a package, you should execute it as a module to ensure imports work correctly. Run this command from the project's root directory:
  ```bash
  python -m painpoint_pipeline.process_batch
  ```

## Testing

The project includes a suite of tests to verify core functionality. To run the tests, execute the following command from the project's root directory:

```bash
pytest
```

## Output

  - **`pain_points.csv`:** A CSV file where each row represents a processed screenshot.
  - **`Archived/`:** A folder containing all the screenshots that have been successfully processed.
  - **`ocr_pipeline.log`:** A log file that records the script's operations and any errors encountered.
