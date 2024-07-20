import os
import tempfile
import pytest
import shutil
from fastapi.testclient import TestClient
from api.server import app, UPLOAD_DIR, TEST_FILE_DIR, OUTPUT_DIR

client = TestClient(app)


@pytest.fixture
def setup_test_env():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    for file in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    
    yield UPLOAD_DIR

    # Clean test PDF files
    for file in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    for file in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

def test_upload_files_success(setup_test_env):
    test_file_paths = []
    test_files = os.listdir(TEST_FILE_DIR)
    for test_file in test_files:
        test_file_path = os.path.join(TEST_FILE_DIR, test_file)
        if os.path.isfile(test_file_path):
            test_file_paths.append(("files", (test_file, open(test_file_path, "rb"), "application/pdf")))
    print(test_file_paths)
    
    response = client.post("/upload_files", files = test_file_paths)

    for _, (file_path, file, _) in test_file_paths:
        file.close()

    assert response.status_code==200

    upload_files = os.listdir(setup_test_env)
    assert len(upload_files)==len(test_files)
    for upload_file in upload_files:
        assert os.path.isfile(os.path.join(UPLOAD_DIR, upload_file))

def test_upload_files_unsupported_format(setup_test_env):
    unsupported_file_path = os.path.join(TEST_FILE_DIR, "unsupported.txt")
    with open(unsupported_file_path, "w") as f:
        f.write("Test unsupported text file")
    response = client.post("/upload_files", files=[("files", ("unsupported.txt", open(unsupported_file_path, "rb"), "text/plain"))] )
    assert response.status_code == 400

    os.unlink(unsupported_file_path)


def test_merge_pdfs_success(setup_test_env):
    for test_file in os.listdir(TEST_FILE_DIR):
        test_file_path = os.path.join(TEST_FILE_DIR, test_file)
        if os.path.isfile(test_file_path):
            shutil.copy(test_file_path, UPLOAD_DIR)

    response = client.post(
        "/merge_pdfs", json={"folder": UPLOAD_DIR, "output_path": OUTPUT_DIR}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["output_path"] == OUTPUT_DIR + "/merged_pdf.pdf"
    assert os.path.exists(OUTPUT_DIR), "Output file does not exist"


def test_merge_pdfs_folder_not_exist():
    response = client.post(
        "/merge_pdfs",
        json={"folder": "non_existent_folder", "output_path": "output.pdf"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Folder does not exist"}
