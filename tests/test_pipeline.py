# tests/test_pipeline.py

import pytest
import csv
from PIL import Image, ImageDraw
from pathlib import Path

# Import the functions and class from your main script
from process_batch import (
    get_text_from_image,
    archive_file,
    append_to_csv,
    PainPoint
)

# A pytest fixture to create a temporary test image
@pytest.fixture
def temp_image_file(tmp_path):
    """Creates a temporary PNG image file with text."""
    img_path = tmp_path / "test_image.png"
    img = Image.new('RGB', (200, 50), color = 'white')
    d = ImageDraw.Draw(img)
    d.text((10,10), "Hello pytest!", fill=(0,0,0))
    img.save(img_path)
    return img_path

def test_get_text_from_image(temp_image_file):
    """Tests that the OCR function correctly extracts text."""
    # Action
    extracted_text = get_text_from_image(temp_image_file)
    # Assertion
    assert "Hello pytest!" in extracted_text

def test_archive_file(tmp_path):
    """Tests that the archive function correctly moves a file."""
    # Setup
    source_dir = tmp_path / "source"
    archive_dir = tmp_path / "archive"
    source_dir.mkdir()
    archive_dir.mkdir()
    test_file = source_dir / "test.txt"
    test_file.touch() # Create an empty file

    # Action
    archive_file(test_file, archive_dir)

    # Assertions
    assert not test_file.exists()
    assert (archive_dir / "test.txt").exists()

def test_append_to_csv(tmp_path):
    """Tests that data is correctly appended to a CSV file."""
    # Setup
    db_file = tmp_path / "test.csv"
    test_entry = PainPoint(
        pain_point_id="test-id-123",
        date_observed="2025-08-12",
        source_platform="Test",
        raw_text="This is a test.",
        screenshot_link="test.png"
    )

    # Action
    append_to_csv(test_entry, db_file)

    # Assertion
    with open(db_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = next(reader)
    
    assert header[0] == "pain_point_id"
    assert data[0] == "test-id-123"
    assert data[4] == "test.png"