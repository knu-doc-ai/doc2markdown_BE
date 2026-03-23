import os
import json
from fastapi.testclient import TestClient
from app.main import app  # Assuming main.py is in the root of BE

client = TestClient(app)

def run_tests():
    # Create a dummy pdf file
    dummy_pdf_content = b"%PDF-1.4\n%..."
    
    files = {
        'file': ('test_upload.pdf', dummy_pdf_content, 'application/pdf')
    }
    
    print("Sending POST request to /documents/upload ...")
    response = client.post("/documents/upload", files=files)
    
    print(f"Response Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    
    if response.status_code != 201:
        print("TEST FAILED: Expected status code 201")
        return
        
    data = response.json()
    document_id = data.get("documentId")
    
    # Check if files were created
    storage_path = f"storage/documents/{document_id}"
    pdf_path = f"{storage_path}/original.pdf"
    meta_path = f"{storage_path}/meta.json"
    
    print(f"Checking if paths exist...")
    print(f"Dir exists: {os.path.exists(storage_path)}")
    print(f"PDF exists: {os.path.exists(pdf_path)}")
    print(f"Meta exists: {os.path.exists(meta_path)}")
    
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)
            print("Meta content:", meta)
            
    if os.path.exists(storage_path):
        # Clean up
        import shutil
        shutil.rmtree(storage_path)
        print(f"Cleaned up {storage_path}")

if __name__ == "__main__":
    run_tests()
