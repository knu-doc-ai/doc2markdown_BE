import os
import json
import shutil
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    dummy_pdf_content = b"%PDF-1.4\n%..."
    files = {'file': ('test_upload.pdf', dummy_pdf_content, 'application/pdf')}

    # ── [1] POST /documents/upload ──────────────────────
    print("=" * 50)
    print("[1] POST /documents/upload")
    response = client.post("/documents/upload", files=files)
    print(f"  Status: {response.status_code}  (expected: 201)")
    print(f"  Body:   {response.json()}")

    if response.status_code != 201:
        print("  ❌ FAILED: Expected 201")
        return

    document_id = response.json().get("documentId")
    storage_path = f"storage/documents/{document_id}"

    # ── [2] GET /documents/{documentId}/status — 정상 ──
    print("\n[2] GET /documents/{documentId}/status — 정상 케이스")
    res_status = client.get(f"/documents/{document_id}/status")
    print(f"  Status: {res_status.status_code}  (expected: 200)")
    print(f"  Body:   {res_status.json()}")

    assert res_status.status_code == 200,                       "❌ Expected 200"
    assert res_status.json()["status"] == "UPLOADED",          "❌ status should be UPLOADED"
    assert res_status.json()["documentId"] == document_id,     "❌ documentId mismatch"
    assert res_status.json()["fileName"] == "test_upload.pdf", "❌ fileName mismatch"
    print("  ✅ PASSED")

    # ── [3] GET /documents/{documentId}/status — 404 ───
    print("\n[3] GET /documents/nonexistent_id/status — 404 케이스")
    res_404 = client.get("/documents/nonexistent_id/status")
    print(f"  Status: {res_404.status_code}  (expected: 404)")

    assert res_404.status_code == 404, "❌ Expected 404"
    print("  ✅ PASSED")

    # ── Cleanup ─────────────────────────────────────────
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
        print(f"\n🧹 Cleaned up {storage_path}")

    print("\n✅ All tests passed!")

if __name__ == "__main__":
    run_tests()
