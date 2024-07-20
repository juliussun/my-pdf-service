import os
import pymupdf
import pytest
import tempfile
from api.pdfmerger_alternative import pdf_merger

@pytest.fixture
def setup_test_env():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_folder = os.path.join(temp_dir, "test_pdfs")
        os.makedirs(test_folder, exist_ok=True)
        for i in range(3):
            doc = pymupdf.open()
            page = doc.new_page(width=72, height=72)  # type: ignore
            page.insert_text((36,36), f"Text {i}")
            doc.save(os.path.join(test_folder, f"test_{i}.pdf"))
        yield test_folder

def test_pdf_merger_ouput_path(setup_test_env:str):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_folder = os.path.join(temp_dir, "test_output")
        os.makedirs(output_folder, exist_ok=True)

        result = pdf_merger(setup_test_env, output_folder)
        output_path = result.get("output_path")

        assert output_path is not None, "Output path is not in the result"
        assert os.path.exists(output_path), "Output file does not exist"

def test_pdf_merger_page_count(setup_test_env):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_folder = os.path.join(temp_dir, "test_output")
        os.makedirs(output_folder, exist_ok=True)

        result = pdf_merger(setup_test_env, output_folder)
        output_path = result.get("output_path")

        doc = pymupdf.open(output_path)
        assert doc.page_count == 3, "Output PDF does not have the expeted number"

def test_pdf_merger_page_content(setup_test_env):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_folder = os.path.join(temp_dir, "test_output")
        os.makedirs(output_folder, exist_ok=True)

        result = pdf_merger(setup_test_env, output_folder)
        output_path = result.get("output_path")

        doc = pymupdf.open(output_path)
        for i in range(3):
            page = doc.load_page(i)
            text = page.get_text("text") # type: ignore
            print(text, f"on page {i}")
            assert f"Text {i}" in text, f"Content of page {i} is incorrect: {text}"

if __name__ == "__main__":
    pytest.main()