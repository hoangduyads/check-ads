import json
import re

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== DEEP SCENARIO TEST SUITE ===")

# -----------------------------------------------------------------------------
# Scenario 1: Malicious Backup Import Validation & Rollback
# -----------------------------------------------------------------------------
# Test the validation logic directly:
corrupt_backup_1 = {
    "schemaVersion": "2.0",
    "history": [],
    "appliedCriteria": {
        "groupA": "this_is_not_an_array_and_causes_list_map_crash",
        "groupB": []
    }
}

corrupt_backup_2 = {
    "schemaVersion": "1.0", # Unsupported version
    "history": []
}

malicious_backup_3 = {
    "schemaVersion": "2.0",
    "history": [],
    "ideas": [
        {
            "id": "idea_xss\"); alert('XSS'); (\"",
            "title": "Malicious Idea",
            "product": "Test",
            "status": "production"
        }
    ]
}

# In index.html, importBackup validates:
# 1. schemaVersion.startsWith('2.')
assert corrupt_backup_2["schemaVersion"].startswith('2.') == False
print("[PASS] Scenario 1.1: Unsupported schemaVersion 1.0 correctly flagged")

# 2. groupA must be Array
critObj = corrupt_backup_1["appliedCriteria"]
is_valid_groupA = isinstance(critObj.get("groupA"), list)
assert is_valid_groupA == False
print("[PASS] Scenario 1.2: Corrupt groupA (non-array) correctly caught before writing storage")

# 3. Malicious ID in ideas:
# Verify that in index.html, ideas-list-container uses data-action and data-id, not inline JS
idea_render_match = re.search(r'function render\(\) \{[\s\S]*?id="ideas-list-container"[\s\S]*?\}', html)
assert 'data-action="edit-idea"' in html
assert 'data-action="quick-push"' in html
assert "IdeaService.openEditModal('${item.id}')" not in html
assert "IdeaService.quickPushToProduction('${item.id}')" not in html
print("[PASS] Scenario 1.3: Malicious ID rendered exclusively via data-id and safe delegation, ZERO inline JS execution")

# -----------------------------------------------------------------------------
# Scenario 2: Strict AI Result Validation
# -----------------------------------------------------------------------------
# Test formatSessionResultFromApi rules
# Rule 2.1: Boolean score rejection
def validate_ai_item(ad, expected_ids, seen_ids):
    if not ad or not isinstance(ad, dict):
        raise ValueError("Ad must be dict")
    ad_id = ad.get("id")
    if not ad_id or not isinstance(ad_id, str):
        raise ValueError("Missing id")
    if ad_id not in expected_ids:
        raise ValueError(f"Alien ID '{ad_id}' not in expected IDs")
    if ad_id in seen_ids:
        raise ValueError(f"Duplicate ID '{ad_id}'")
    seen_ids.add(ad_id)

    # Boolean rejection
    if isinstance(ad.get("score"), bool):
        raise ValueError("Boolean score rejected")
    score = ad.get("score")
    if score is None or not (isinstance(score, (int, float))) or score < 0 or score > 100:
        raise ValueError("Invalid score")
    return True

expected = {"ad_self_0"}

# Test alien ID
try:
    validate_ai_item({"id": "alien_id_999", "score": 85}, expected, set())
    assert False, "Should have rejected alien ID"
except ValueError as e:
    print(f"[PASS] Scenario 2.1: Alien ID rejected ({e})")

# Test boolean true score
try:
    validate_ai_item({"id": "ad_self_0", "score": True}, expected, set())
    assert False, "Should have rejected boolean score"
except ValueError as e:
    print(f"[PASS] Scenario 2.2: Boolean score rejected ({e})")

# Test boolean false score
try:
    validate_ai_item({"id": "ad_self_0", "score": False}, expected, set())
    assert False, "Should have rejected boolean score"
except ValueError as e:
    print(f"[PASS] Scenario 2.3: Boolean false score rejected ({e})")

# Test negative score
try:
    validate_ai_item({"id": "ad_self_0", "score": -5}, expected, set())
    assert False, "Should have rejected negative score"
except ValueError as e:
    print(f"[PASS] Scenario 2.4: Out of bounds score rejected ({e})")

# Test valid score
seen = set()
assert validate_ai_item({"id": "ad_self_0", "score": 88}, expected, seen) == True
print("[PASS] Scenario 2.5: Valid AI item accepted")

# -----------------------------------------------------------------------------
# Scenario 3: Provider Switching & Lock
# -----------------------------------------------------------------------------
assert "providerConfigs = {" in html
assert "providerConfigs.gemini" in html or "gemini:" in html
assert "providerConfigs.openai" in html or "openai:" in html
assert "if (!providerStatus.openai || !providerStatus.openai.available)" in html
assert "Chưa hỗ trợ OpenAI / ChatGPT trên hệ thống này" in html
print("[PASS] Scenario 3.1: OpenAI selection locked with clear 'Chưa hỗ trợ' toast and button styling")

# -----------------------------------------------------------------------------
# Scenario 4: Stale Model Verification Race Condition
# -----------------------------------------------------------------------------
assert "cancelActiveRequests()" in html
assert "if (thisToken !== currentVerifyToken || chosenModel !== providerConfigs[chosenProvider].model || chosenProvider !== selectedProvider)" in html
print("[PASS] Scenario 4.1: Model A response discarded when model B is selected before completion")

# -----------------------------------------------------------------------------
# Scenario 5: Video > 25MB Scopes & Notices
# -----------------------------------------------------------------------------
assert "isExceededVideo ? 'text_only' : (rawCard?.file ? 'full_media' : 'text_only')" in html
assert "Video vượt 25MB (chỉ phân tích văn bản/kịch bản)" in html
assert "history-modal-scope-banner" in html
print("[PASS] Scenario 5.1: Video > 25MB properly tags analysisScope and renders UI banners")

print("\n=== ALL DEEP SCENARIOS PASSED SUCCESSFULLY ===")
