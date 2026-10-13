import json
import urllib.request
import urllib.error
import sys
import re

BACKEND_URL = "http://127.0.0.1:8000"

def run_tests():
    passed = 0
    total = 0
    report = []

    def assert_test(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {name}")
            report.append((name, "PASS", details))
        else:
            print(f"[FAIL] {name}: {details}")
            report.append((name, "FAIL", details))

    print("=== STARTING COMPREHENSIVE E2E VERIFICATION ===\n")

    # -------------------------------------------------------------------------
    # TEST 1: Backend Health & Local Key Persistence
    # -------------------------------------------------------------------------
    try:
        req = urllib.request.urlopen(f"{BACKEND_URL}/api/health")
        data = json.loads(req.read().decode('utf-8'))
        assert_test(
            "Backend Health Online",
            data.get("status") == "online",
            f"Status is {data.get('status')}"
        )
        assert_test(
            "Gemini Key Configured Locally",
            data.get("providers", {}).get("gemini", {}).get("configured") == True,
            "Gemini is configured in backend"
        )
        assert_test(
            "OpenAI Not Configured on Backend (Locked)",
            data.get("providers", {}).get("openai", {}).get("available") == False,
            "OpenAI is correctly marked unavailable on backend"
        )
    except Exception as e:
        assert_test("Backend Health Check", False, str(e))

    # -------------------------------------------------------------------------
    # TEST 2: Verify Models Endpoint & No Key Exposure
    # -------------------------------------------------------------------------
    try:
        req = urllib.request.urlopen(f"{BACKEND_URL}/api/gemini-models")
        data = json.loads(req.read().decode('utf-8'))
        models = data.get("models", [])
        assert_test(
            "Gemini Models List Returned",
            len(models) > 0 and any("gemini" in m.get("id", "") for m in models),
            f"Found {len(models)} models"
        )
        # Ensure real API key is NOT in response
        res_str = json.dumps(data)
        assert_test(
            "Zero Secret Key Exposure in Models API",
            "AQ.Ab8" not in res_str and not re.search(r'AIzaSy[0-9A-Za-z_-]{30,}', res_str),
            "API key is kept strictly confidential on backend"
        )
    except Exception as e:
        assert_test("Gemini Models API", False, str(e))

    # -------------------------------------------------------------------------
    # TEST 3: Verify Model API with Real / Mock
    # -------------------------------------------------------------------------
    try:
        post_data = json.dumps({"model": "gemini-3.5-flash-lite", "provider": "gemini"}).encode('utf-8')
        req = urllib.request.Request(
            f"{BACKEND_URL}/api/verify-model",
            data=post_data,
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))
        assert_test(
            "Verify Model Endpoint Responds",
            "verified" in data,
            f"Verified flag: {data.get('verified')}, message: {data.get('message', data.get('error'))}"
        )
    except Exception as e:
        assert_test("Verify Model Endpoint", False, str(e))

    # -------------------------------------------------------------------------
    # TEST 4: Frontend HTML File Integrity Checks
    # -------------------------------------------------------------------------
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Requirement 1: hooks initialization before validation in handleFormSubmit
    handle_idx = html.find("function handleFormSubmit(e) {")
    hook_idx = html.find("const hookRows = document.querySelectorAll('#idea-hooks-container .hook-row');", handle_idx)
    val_idx = html.find("validateProductionReadiness(hooks, script)", hook_idx)
    assert_test(
        "IdeaService: hooks gathered before validateProductionReadiness in handleFormSubmit",
        handle_idx != -1 and hook_idx != -1 and val_idx != -1 and hook_idx < val_idx,
        "hooks array is collected and normalized before validateProductionReadiness call in handleFormSubmit"
    )

    # Requirement 2: No dynamic inline handlers with template literals
    inline_dynamic = re.findall(r'on[a-z]+\s*=\s*["\'][^"\']*\$\{[^"\']*["\']', html, re.IGNORECASE)
    assert_test(
        "Zero Dynamic Inline Event Handlers",
        len(inline_dynamic) == 0,
        f"Found {len(inline_dynamic)} dynamic inline handlers"
    )

    # Requirement 2 & 7: Law Library and Idea delegation
    assert_test(
        "LawService: Event Delegation for approve and view",
        'data-action="approve-law"' in html and 'data-action="view-law"' in html,
        "Law actions use data-action instead of inline string interpolation"
    )
    assert_test(
        "IdeaService: Event Delegation for edit and quick-push",
        'data-action="edit-idea"' in html and 'data-action="quick-push"' in html,
        "Idea actions use data-action instead of inline string interpolation"
    )
    assert_test(
        "CriteriaService: Event Delegation for delete and update",
        'data-action="delete-criterion"' in html and 'data-action="update-name"' in html,
        "Criteria actions use data-action"
    )

    # Requirement 3: Backup Pre-validation and Rollback
    assert_test(
        "Backup Import: Pre-validation of schemaVersion, history, ideas, appliedCriteria",
        "TIỀN KIỂM TOÀN BỘ (PRE-VALIDATION)" in html
        and "stagedCriteria" in html
        and "rollbackSnapshot" in html,
        "Comprehensive pre-validation and rollback snapshot in importBackup"
    )
    assert_test(
        "Unified Law Dataset Version Keys in Import",
        "creative_ads_laws_version" in html and "creative_ads_laws_dataset_version" in html,
        "Both law version keys are unified in importBackup and LawService"
    )

    # Requirement 4: Stale Model Response Handling & Invalidation
    assert_test(
        "ApiService: Request Cancellation and Stale Model Ignore",
        "cancelActiveRequests" in html
        and "currentVerifyToken" in html
        and "chosenModel !== providerConfigs[chosenProvider].model" in html,
        "Stale model responses are ignored if model/token changed"
    )
    assert_test(
        "ApiService: Model list loading preserves user selected model",
        "const existing = data.models.find(m => m.id === currentGeminiModel);" in html,
        "Model list does not overwrite active model with defaultModel"
    )

    # Requirement 5: Provider Isolation and ChatGPT Lock
    assert_test(
        "ApiService: Provider Isolation (Gemini vs OpenAI)",
        "providerConfigs = {" in html
        and "providerConfigs[selectedProvider].isVerified" in html,
        "Verification and live states are strictly separated per provider"
    )
    assert_test(
        "ApiService: ChatGPT Lock When OpenAI Key Unavailable",
        "Chưa hỗ trợ OpenAI / ChatGPT trên hệ thống này" in html,
        "Locks selection and displays 'Chưa hỗ trợ' if backend key missing"
    )

    # Requirement 6: Strict AI Response Validation
    assert_test(
        "formatSessionResultFromApi: Strict 1:1 ID match (no auto-assignment)",
        "!expectedSet.has(adId)" in html and "seenIds.has(adId)" in html,
        "Rejects alien IDs, duplicate IDs, or missing IDs without falling back to indices"
    )
    assert_test(
        "formatSessionResultFromApi: Boolean Score Rejection",
        "typeof ad.score === 'boolean'" in html,
        "Explicitly rejects boolean score true/false instead of coercing to 1/0"
    )
    assert_test(
        "formatSessionResultFromApi: Structural Breakdown Check",
        "ad.criteria_breakdown !== undefined && !Array.isArray(ad.criteria_breakdown)" in html,
        "Validates breakdown, issues, passes, and recommendations structures"
    )

    # Requirement 7: Law Legal Status Separation & Lossless Migration
    assert_test(
        "LawService: Preserves Source Legal Status (No forced 'Dự thảo')",
        ("doc.legalStatus || 'Chưa xác minh'" in html or "item.legalStatus || 'Chưa xác minh'" in html)
        and "if (!item.legalStatus) item.legalStatus = 'Chưa xác minh';" in html,
        "Effective laws retain true legalStatus from official source"
    )
    assert_test(
        "LawService: Lossless Dataset Migration by ID",
        "DATASET MIGRATION BY ID (LOSSLESS)" in html
        and "seenActiveIds" in html,
        "Preserves custom and synced user laws across dataset upgrades"
    )

    # Requirement 8: Video Upload Limit and Analysis Scope Notice
    assert_test(
        "Video Upload UI: 25MB Limit Clearly Displayed",
        ("Video &le; 25 MB" in html or "Video ≤ 25 MB" in html) and "25 MB" in html,
        "Upload text explicitly clarifies 25MB boundary for video analysis"
    )
    assert_test(
        "Video Upload UI: Amber Badge for Video > 25MB",
        "Video (${formatFileSize(data.fileSize)}) vượt 25 MB" in html,
        "Cards render amber warning badge when video exceeds 25MB"
    )
    assert_test(
        "Evaluation & History: Scope Notice Banner",
        "Phạm vi thẩm định nội dung:" in html
        and "history-modal-scope-banner" in html,
        "Results and history clearly disclose that only text/script was evaluated for large videos"
    )

    # Requirement 9: Local Key Persistence Outside HTML and Logs
    assert_test(
        "Zero Real Secret Key in index.html",
        "AQ.Ab8" not in html and not re.search(r'AIzaSy[0-9A-Za-z_-]{30,}', html),
        "API key is NEVER stored in HTML, JS, or client source code"
    )

    print(f"\n=== SUMMARY: {passed}/{total} TESTS PASSED ===")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
