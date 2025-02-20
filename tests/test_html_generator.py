import os
import pytest
from app.utils.html_generator import generate_html

def test_generate_html():
    image_files = ["page1.png", "page2.png", "page3.png"]
    title = "Test Flipbook"
    html_content = generate_html(image_files, title)

    assert "<title>Test Flipbook</title>" in html_content
    for idx, img in enumerate(image_files):
        assert f'<img src="{os.path.basename(img)}" alt="Page {idx+1}">' in html_content
    assert '<link rel="stylesheet" href="css/flipbook.css">' in html_content