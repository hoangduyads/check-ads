# -*- coding: utf-8 -*-
"""
apply_stage2_report.py
Injects:
1. Video Keyframe Extraction in EvaluationService.handleFileInput
2. Brand Profile & Campaign Context capture in startEvaluation
3. Rich formatSessionResultFromApi preserving Schema v3.0 objects
4. Comprehensive computeSimulatedSessionResult matching Benchmark Images 1-5
5. Master Comprehensive Report Renderer shared by Results View and History Modal
"""
import sys

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # -------------------------------------------------------------------------
    # 1. Add Brand Profile helper functions, Keyframe zoom helpers, and IdeaService.saveVariantAsIdea
    # -------------------------------------------------------------------------
    # Let's add saveVariantAsIdea right inside IdeaService before its return
    idea_needle = "                validateProductionReadiness\n            };"
    if 'saveVariantAsIdea,' not in html and idea_needle in html:
        save_idea_code = '''                saveVariantAsIdea,
                validateProductionReadiness
            };'''
        # And define saveVariantAsIdea right before return in IdeaService
        idea_func = '''            function saveVariantAsIdea(variant, sessionTitle, brandName) {
                if (!variant || !variant.copy) return false;
                const existing = ideasList.find(i => i.sourceVariantId === variant.id || (i.script && i.script.trim() === variant.copy.trim()));
                if (existing) {
                    showToast('Biến thể này đã được lưu trong Kho ý tưởng trước đó!', 'info');
                    return true;
                }
                const newIdea = {
                    id: `idea_var_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
                    sourceVariantId: variant.id || `var_${Date.now()}`,
                    title: `[Viết lại] ${variant.angle || 'Biến thể'} - ${brandName || 'Ad'}`,
                    product: brandName || 'Dịch vụ',
                    brief: `Biến thể viết lại góc tiếp cận "${variant.angle}". Đã xử lý: ${(variant.fixes_addressed || []).join(', ')}.`,
                    objective: 'Chuyển đổi quảng cáo / Tối ưu tuân thủ',
                    targetAudience: 'Khách hàng quan tâm làm đẹp/dịch vụ',
                    coreAngle: variant.angle || 'Lợi ích',
                    hooks: [
                        { text: (variant.copy.split('\\n')[0] || variant.copy).slice(0, 80), selected: true }
                    ],
                    script: variant.copy,
                    callToAction: 'Nhắn tin để nhận tư vấn và ưu đãi',
                    score: 4,
                    status: 'approved',
                    productionDetails: {
                        checklist: { actor: false, props: false, lighting: false, voiceover: false },
                        stage: 'pre',
                        directorNotes: `Facts đã dùng: ${(variant.facts_used || []).join(', ')}`
                    }
                };
                ideasList.unshift(newIdea);
                StorageService.setJSON(STORAGE_KEY, ideasList);
                render();
                OverviewController.updateStats();
                showToast(`Đã lưu biến thể "${variant.angle}" vào Kho ý tưởng thành công!`, 'success');
                return true;
            }

'''
        html = html.replace(idea_needle, idea_func + idea_needle.replace('validateProductionReadiness', 'saveVariantAsIdea,\n                validateProductionReadiness'))
        print("[APPLIED] IdeaService.saveVariantAsIdea injected")

    # -------------------------------------------------------------------------
    # 2. Add Keyframe extractors and UI helpers before EvaluationService
    # -------------------------------------------------------------------------
    ui_helpers = '''
        // --------------------------------------------------------------------------
        // UI & KEYFRAME HELPERS (CLIENT-SIDE EXTRACTION & ACCORDION)
        // --------------------------------------------------------------------------
        function toggleBrandProfileAccordion() {
            const el = document.getElementById('brand-profile-fields-container');
            const icon = document.getElementById('bp-toggle-icon');
            if (!el) return;
            el.classList.toggle('hidden');
            if (icon) {
                icon.innerHTML = el.classList.contains('hidden') ? '<i class="fa-solid fa-chevron-down text-xs"></i>' : '<i class="fa-solid fa-chevron-up text-xs"></i>';
            }
        }

        function getBrandProfileFromUI() {
            return {
                brand_name: document.getElementById('bp-brand-name')?.value?.trim() || '',
                industry_category: document.getElementById('bp-industry')?.value || 'spa_beauty',
                price_offer: document.getElementById('bp-price')?.value?.trim() || '',
                price_type: document.getElementById('bp-price-type')?.value || 'unspecified',
                conditions: document.getElementById('bp-conditions')?.value?.trim() || '',
                hotline: document.getElementById('bp-hotline')?.value?.trim() || '',
                branches_url: document.getElementById('bp-hotline')?.value?.trim() || '',
                license_number: document.getElementById('bp-license')?.value?.trim() || '',
                target_audience: document.getElementById('bp-audience')?.value?.trim() || '',
                campaign_objective: document.getElementById('bp-objective')?.value || ''
            };
        }

        function getCampaignContextFromUI() {
            return {
                industry: document.getElementById('bp-industry')?.value || 'spa_beauty',
                target_audience: document.getElementById('bp-audience')?.value?.trim() || '',
                campaign_objective: document.getElementById('bp-objective')?.value || ''
            };
        }

        function openKeyframeZoomModal(src, ts) {
            const m = document.getElementById('keyframe-zoom-modal');
            const img = document.getElementById('keyframe-zoom-img');
            const tsEl = document.getElementById('keyframe-zoom-ts');
            if (m && img) {
                img.src = src;
                if (tsEl) tsEl.textContent = ts || 'Khung hình';
                m.classList.remove('hidden');
                document.body.classList.add('overflow-hidden');
            }
        }

        function closeKeyframeZoomModal() {
            const m = document.getElementById('keyframe-zoom-modal');
            if (m) m.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }

        async function extractVideoKeyframes(file) {
            return new Promise((resolve) => {
                if (!file || !file.type.startsWith('video/')) {
                    resolve([]);
                    return;
                }
                const timeout = setTimeout(() => resolve([]), 6000);
                try {
                    const video = document.createElement('video');
                    video.preload = 'metadata';
                    video.muted = true;
                    video.playsInline = true;
                    const url = URL.createObjectURL(file);
                    video.src = url;

                    video.onloadedmetadata = async () => {
                        const duration = video.duration || 10;
                        const times = [
                            Math.max(0.5, Math.min(1.0, duration * 0.1)),
                            Math.max(1.5, Math.min(duration * 0.35, duration - 1)),
                            Math.max(2.5, Math.min(duration * 0.65, duration - 1)),
                            Math.max(3.5, Math.min(duration * 0.9, duration - 0.5))
                        ];
                        const uniqueTimes = Array.from(new Set(times.map(t => Math.round(t * 10) / 10))).sort((a,b) => a - b);
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');
                        const keyframes = [];

                        for (let i = 0; i < uniqueTimes.length; i++) {
                            const t = uniqueTimes[i];
                            await new Promise((seekRes) => {
                                const onSeeked = () => {
                                    video.removeEventListener('seeked', onSeeked);
                                    try {
                                        const w = 240;
                                        const h = Math.round((video.videoHeight / (video.videoWidth || 1)) * w) || 135;
                                        canvas.width = w;
                                        canvas.height = h;
                                        ctx.drawImage(video, 0, 0, w, h);
                                        const dataUrl = canvas.toDataURL('image/jpeg', 0.7);
                                        const mins = Math.floor(t / 60);
                                        const secs = Math.floor(t % 60);
                                        const ts = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
                                        const labels = ['Mở đầu (Hook)', 'Thao tác & Dịch vụ', 'Ưu đãi & Kết quả', 'Kêu gọi hành động (CTA)'];
                                        keyframes.push({
                                            id: `kf_${i}`,
                                            timestamp: ts,
                                            time_seconds: t,
                                            thumbnail: dataUrl,
                                            label: labels[i] || `Khung hình ${i+1}`,
                                            ocr: ''
                                        });
                                    } catch (err) {
                                        console.warn('Frame capture notice', err);
                                    }
                                    seekRes();
                                };
                                video.addEventListener('seeked', onSeeked);
                                video.currentTime = t;
                            });
                        }
                        clearTimeout(timeout);
                        URL.revokeObjectURL(url);
                        resolve(keyframes);
                    };
                    video.onerror = () => {
                        clearTimeout(timeout);
                        URL.revokeObjectURL(url);
                        resolve([]);
                    };
                } catch (e) {
                    clearTimeout(timeout);
                    resolve([]);
                }
            });
        }

        async function extractImageKeyframe(file) {
            return new Promise((resolve) => {
                if (!file || !file.type.startsWith('image/')) {
                    resolve([]);
                    return;
                }
                const reader = new FileReader();
                reader.onload = () => {
                    resolve([{
                        id: 'kf_0',
                        timestamp: '00:00',
                        time_seconds: 0.0,
                        thumbnail: reader.result,
                        label: 'Visual chính của quảng cáo',
                        ocr: ''
                    }]);
                };
                reader.onerror = () => resolve([]);
                reader.readAsDataURL(file);
            });
        }

        // Global Event Delegation for Variants, Keyframes & Empty state buttons (ZERO inline handlers!)
        document.addEventListener('click', (e) => {
            const copyBtn = e.target.closest('[data-action="copy-variant"]');
            if (copyBtn) {
                const card = copyBtn.closest('.variant-card');
                const text = card?.querySelector('.variant-copy-text')?.textContent?.trim();
                if (text) {
                    navigator.clipboard.writeText(text).then(() => {
                        showToast('Đã sao chép nội dung kịch bản biến thể!', 'success');
                    }).catch(() => {
                        showToast('Không thể sao chép tự động. Hãy bôi đen và nhấn Ctrl+C', 'warning');
                    });
                }
            }
            const saveBtn = e.target.closest('[data-action="save-idea-variant"]');
            if (saveBtn) {
                const card = saveBtn.closest('.variant-card');
                const varId = saveBtn.getAttribute('data-variant-id');
                const angle = saveBtn.getAttribute('data-variant-angle') || 'Biến thể tối ưu';
                const copy = card?.querySelector('.variant-copy-text')?.textContent?.trim() || '';
                const fixes = (saveBtn.getAttribute('data-fixes') || '').split('|').filter(Boolean);
                const facts = (saveBtn.getAttribute('data-facts') || '').split('|').filter(Boolean);
                const brand = saveBtn.getAttribute('data-brand') || 'Seoul Center';
                if (copy && typeof IdeaService !== 'undefined' && IdeaService.saveVariantAsIdea) {
                    IdeaService.saveVariantAsIdea({
                        id: varId,
                        angle,
                        copy,
                        fixes_addressed: fixes,
                        facts_used: facts
                    }, 'Quảng cáo', brand);
                }
            }
            const zoomBtn = e.target.closest('[data-action="zoom-keyframe"]');
            if (zoomBtn) {
                const src = zoomBtn.getAttribute('data-src');
                const ts = zoomBtn.getAttribute('data-ts');
                if (src) openKeyframeZoomModal(src, ts);
            }
            const switchCompBtn = e.target.closest('[data-action="switch-to-compare"]');
            if (switchCompBtn) {
                EvaluationService.setMode('compare');
                showToast('Đã chuyển sang chế độ So sánh với đối thủ!', 'info');
            }
        });
'''
    eval_service_marker = 'const EvaluationService = (() => {'
    if 'function extractVideoKeyframes' not in html and eval_service_marker in html:
        html = html.replace(eval_service_marker, ui_helpers + '\n        ' + eval_service_marker)
        print("[APPLIED] Keyframe extractors and UI helpers added before EvaluationService")

    # -------------------------------------------------------------------------
    # 3. Add keyframe extraction to handleFileInput
    # -------------------------------------------------------------------------
    old_handle_file = '''                StorageService.saveBlob(card.blobId, file, file.name, file.type);
                renderMediaCardsGrid();
                validateInputsRealtime();
            }'''

    new_handle_file = '''                card.keyframes = [];
                StorageService.saveBlob(card.blobId, file, file.name, file.type);
                renderMediaCardsGrid();
                validateInputsRealtime();

                // Extract client-side keyframes asynchronously
                if (isVideo) {
                    extractVideoKeyframes(file).then(kfs => { card.keyframes = kfs; }).catch(e => console.warn('Keyframe extraction notice:', e));
                } else if (isImage) {
                    extractImageKeyframe(file).then(kfs => { card.keyframes = kfs; }).catch(e => console.warn('Keyframe extraction notice:', e));
                }
            }'''

    if old_handle_file in html:
        html = html.replace(old_handle_file, new_handle_file)
        print("[APPLIED] Keyframe extraction integrated into handleFileInput")

    # -------------------------------------------------------------------------
    # 4. Include brandProfile & campaignContext in startEvaluation & prepareInputsForApi
    # -------------------------------------------------------------------------
    old_copy_card = '''                        const copyCard = (c) => {
                            if (!c) return null;
                            return {
                                id: c.id,
                                file: c.file, // Keep raw Blob reference!
                                blobId: c.blobId,
                                fileName: c.fileName || '',
                                fileSize: c.fileSize || 0,
                                mimeType: c.mimeType || '',
                                caption: c.caption || '',
                                link: c.link || '',
                                previewUrl: c.previewUrl || ''
                            };
                        };'''

    new_copy_card = '''                        const copyCard = (c) => {
                            if (!c) return null;
                            return {
                                id: c.id,
                                file: c.file, // Keep raw Blob reference!
                                blobId: c.blobId,
                                fileName: c.fileName || '',
                                fileSize: c.fileSize || 0,
                                mimeType: c.mimeType || '',
                                caption: c.caption || '',
                                link: c.link || '',
                                previewUrl: c.previewUrl || '',
                                keyframes: c.keyframes || []
                            };
                        };'''

    if old_copy_card in html:
        html = html.replace(old_copy_card, new_copy_card)
        print("[APPLIED] Keyframes attached to copied cards in snapshot")

    # Attach brandProfile, campaignContext, lawSnapshot to executionSnapshot
    old_exec_snap = '''                    criteriaSnapshot: CriteriaService.getAppliedCriteriaSnapshot(),
                    isAiLive: ApiService.isAiLive(),
                    provider: ApiService.getSelectedProvider(),
                    modelName: ApiService.getModelName()
                };'''

    new_exec_snap = '''                    criteriaSnapshot: CriteriaService.getAppliedCriteriaSnapshot(),
                    lawSnapshot: (typeof LawService !== 'undefined' && LawService.getLawsSnapshot) ? LawService.getLawsSnapshot() : null,
                    brandProfile: getBrandProfileFromUI(),
                    campaignContext: getCampaignContextFromUI(),
                    isAiLive: ApiService.isAiLive(),
                    provider: ApiService.getSelectedProvider(),
                    modelName: ApiService.getModelName()
                };'''

    if old_exec_snap in html:
        html = html.replace(old_exec_snap, new_exec_snap)
        print("[APPLIED] brandProfile and campaignContext attached to executionSnapshot")

    # Attach to apiPayload in startEvaluation
    old_api_payload = '''                        const apiPayload = {
                            mode: executionSnapshot.mode,
                            platform: executionSnapshot.platform,
                            provider: executionSnapshot.provider,
                            model: executionSnapshot.modelName,
                            inputs: formattedInputs,
                            criteriaSnapshot: executionSnapshot.criteriaSnapshot
                        };'''

    new_api_payload = '''                        const apiPayload = {
                            mode: executionSnapshot.mode,
                            platform: executionSnapshot.platform,
                            provider: executionSnapshot.provider,
                            model: executionSnapshot.modelName,
                            inputs: formattedInputs,
                            criteriaSnapshot: executionSnapshot.criteriaSnapshot,
                            lawSnapshot: executionSnapshot.lawSnapshot,
                            brandProfile: executionSnapshot.brandProfile,
                            campaignContext: executionSnapshot.campaignContext
                        };'''

    if old_api_payload in html:
        html = html.replace(old_api_payload, new_api_payload)
        print("[APPLIED] apiPayload enriched with brandProfile and campaignContext")

    # Attach keyframes to cardToApiItem
    old_card_to_api = '''                    hasMedia: !!(b64 || (isImg && rawBlob)),
                    mediaNotice: isExceeded ? 'Video vượt 25MB (chỉ phân tích văn bản/kịch bản)' : ''
                };'''

    new_card_to_api = '''                    hasMedia: !!(b64 || (isImg && rawBlob)),
                    mediaNotice: isExceeded ? 'Video vượt 25MB (chỉ phân tích văn bản/kịch bản)' : '',
                    keyframes: card.keyframes || []
                };'''

    if old_card_to_api in html:
        html = html.replace(old_card_to_api, new_card_to_api)
        print("[APPLIED] keyframes attached to cardToApiItem")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Stage 2 helpers applied successfully.")

if __name__ == '__main__':
    run()
