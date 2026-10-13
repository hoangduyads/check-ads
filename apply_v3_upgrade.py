# -*- coding: utf-8 -*-
"""
apply_v3_upgrade.py
Surgically upgrades index.html to Schema v3.0 with full fidelity to the 5 benchmark images.
"""
import re
import sys

def apply_upgrade():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    orig_html = html

    # -------------------------------------------------------------------------
    # 1. Add Brand Profile / Campaign Context accordion in Step 1.5
    # -------------------------------------------------------------------------
    brand_profile_html = '''
                <!-- 2.5 HỒ SƠ THƯƠNG HIỆU & NGỮ CẢNH CHIẾN DỊCH (BRAND PROFILE & CAMPAIGN CONTEXT) -->
                <div class="rounded-2xl bg-cardBg border border-borderBase p-4 md:p-5 space-y-3.5 shadow-lg">
                    <div class="flex items-center justify-between cursor-pointer" onclick="toggleBrandProfileAccordion()">
                        <div class="flex items-center space-x-2.5">
                            <div class="w-8 h-8 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-sm">
                                <i class="fa-solid fa-building-user"></i>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold text-white flex items-center space-x-2">
                                    <span>Hồ sơ thương hiệu & Ngữ cảnh chiến dịch</span>
                                    <span class="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 font-medium">Khuyến nghị xác thực</span>
                                </h4>
                                <p class="text-[11px] text-gray-400">Cung cấp dữ kiện đã xác nhận để AI không suy đoán sai giá, sai ngành hoặc bịa đặt thông tin</p>
                            </div>
                        </div>
                        <button type="button" class="text-gray-400 hover:text-white transition-colors" id="bp-toggle-icon">
                            <i class="fa-solid fa-chevron-down text-xs"></i>
                        </button>
                    </div>

                    <div id="brand-profile-fields-container" class="space-y-3 pt-3 border-t border-borderBase/60">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Ngành hàng / Mô hình cơ sở</label>
                                <select id="bp-industry" class="w-full px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white focus:outline-none focus:border-purple-500">
                                    <option value="spa_beauty">Spa / Thẩm mỹ thông thường (Phun xăm, Chăm sóc da)</option>
                                    <option value="medical_clinic">Phòng khám / Cơ sở y tế chuyên khoa</option>
                                    <option value="cosmetics">Mỹ phẩm & Chăm sóc cá nhân</option>
                                    <option value="health_supplement">Thực phẩm bảo vệ sức khỏe (TPBVSK)</option>
                                    <option value="ecommerce_other">Thương mại điện tử / Khác</option>
                                </select>
                            </div>
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Tên thương hiệu / Cơ sở</label>
                                <input type="text" id="bp-brand-name" placeholder="VD: Seoul Center" class="w-full px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white placeholder-gray-500 focus:outline-none focus:border-purple-500">
                            </div>
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Mức giá / Ưu đãi đã xác nhận</label>
                                <div class="flex space-x-1.5">
                                    <input type="text" id="bp-price" placeholder="VD: 599k" class="w-1/2 px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white placeholder-gray-500 focus:outline-none focus:border-purple-500">
                                    <select id="bp-price-type" class="w-1/2 px-2 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-[11px] text-white focus:outline-none focus:border-purple-500">
                                        <option value="unspecified">Chưa xác định</option>
                                        <option value="full_package">Trọn gói</option>
                                        <option value="starting_at">Giá từ (khởi điểm)</option>
                                        <option value="first_session">Buổi đầu trải nghiệm</option>
                                        <option value="per_treatment">Theo liệu trình</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Điều kiện áp dụng ưu đãi</label>
                                <input type="text" id="bp-conditions" placeholder="VD: Đặt lịch trước trong tuần, 50 suất đầu" class="w-full px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white placeholder-gray-500 focus:outline-none focus:border-purple-500">
                            </div>
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Hotline & Link chi nhánh xác thực</label>
                                <input type="text" id="bp-hotline" placeholder="VD: Hotline 1800... hoặc https://..." class="w-full px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white placeholder-gray-500 focus:outline-none focus:border-purple-500">
                            </div>
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Số giấy phép / Công bố (nếu có)</label>
                                <input type="text" id="bp-license" placeholder="Để trống nếu chưa có tài liệu xác thực" class="w-full px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white placeholder-gray-500 focus:outline-none focus:border-purple-500">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Khách hàng mục tiêu (Target Persona)</label>
                                <input type="text" id="bp-audience" placeholder="VD: Nữ 25-50 tuổi, đô thị, quan tâm làm đẹp, nhạy giá" class="w-full px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white placeholder-gray-500 focus:outline-none focus:border-purple-500">
                            </div>
                            <div>
                                <label class="text-[11px] font-semibold text-gray-300 block mb-1">Mục tiêu chiến dịch (Campaign Goal)</label>
                                <select id="bp-objective" class="w-full px-3 py-2 rounded-xl bg-[#0E121B] border border-borderLight text-xs text-white focus:outline-none focus:border-purple-500">
                                    <option value="messages_lead">Kéo tin nhắn / Tư vấn đặt lịch</option>
                                    <option value="brand_awareness">Nhận diện thương hiệu & Uy tín</option>
                                    <option value="direct_sales">Chuyển đổi mua hàng trực tiếp</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
'''

    step2_marker = '<!-- 3. KHU VỰC ĐẦU VÀO ĐÁNH GIÁ (DYNAMIC CONTAINER) -->'
    if step2_marker in html and 'id="brand-profile-fields-container"' not in html:
        html = html.replace(step2_marker, brand_profile_html + '\n                ' + step2_marker)
        print("[APPLIED] Brand Profile UI added before Step 2")

    # -------------------------------------------------------------------------
    # 2. Keyframe Image Viewer Modal (Modal phóng to ảnh Keyframe)
    # -------------------------------------------------------------------------
    keyframe_modal_html = '''
    <!-- Modal Xem Khung Hình Phóng To -->
    <div id="keyframe-zoom-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md z-50 hidden flex items-center justify-center p-4" onclick="closeKeyframeZoomModal()">
        <div class="max-w-4xl max-h-[90vh] bg-cardBg border border-borderLight rounded-2xl p-4 space-y-3 relative page-fade-in" onclick="event.stopPropagation()">
            <div class="flex items-center justify-between border-b border-borderBase pb-2">
                <span id="keyframe-zoom-title" class="text-xs font-bold text-white flex items-center space-x-2">
                    <i class="fa-solid fa-film text-purple-400"></i>
                    <span id="keyframe-zoom-ts">00:00</span>
                </span>
                <button type="button" onclick="closeKeyframeZoomModal()" class="w-7 h-7 rounded-lg hover:bg-[#0E121B] text-gray-400 hover:text-white flex items-center justify-center">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <div class="flex items-center justify-center overflow-hidden rounded-xl bg-black">
                <img id="keyframe-zoom-img" src="" alt="Keyframe Preview" class="max-h-[75vh] w-auto object-contain">
            </div>
        </div>
    </div>
'''
    if 'id="keyframe-zoom-modal"' not in html:
        # Place before closing body tag
        html = html.replace('</body>', keyframe_modal_html + '\n</body>')
        print("[APPLIED] Keyframe Zoom Modal added")

    # -------------------------------------------------------------------------
    # 3. Add history-modal-comprehensive-report inside #history-detail-modal
    # -------------------------------------------------------------------------
    hist_rec_pattern = r'(<p id="history-modal-recommendation"[\s\S]*?</p>\s*</div>)'
    if 'id="history-modal-comprehensive-report"' not in html and re.search(hist_rec_pattern, html):
        comp_report_div = '''
            <!-- Scope Banner for History Modal -->
            <div id="history-modal-scope-banner" class="hidden p-3.5 rounded-2xl bg-amber-500/15 border border-amber-500/30 text-xs text-amber-300">
                <i class="fa-solid fa-triangle-exclamation mr-1.5 text-amber-400"></i>
                <strong>Phạm vi thẩm định nội dung:</strong> Video &gt; 25MB được thẩm định dựa trên văn bản/kịch bản (không gửi visual video sang AI).
            </div>

            <!-- Báo Cáo Chuyên Sâu Đồng Bộ (Master Comprehensive Report) -->
            <div id="history-modal-comprehensive-report" class="space-y-6 pt-4 border-t border-borderBase">
                <!-- Sẽ được render bởi renderComprehensiveReport -->
            </div>
'''
        html = re.sub(hist_rec_pattern, r'\1\n' + comp_report_div, html, count=1)
        print("[APPLIED] Comprehensive Report container added to history-detail-modal")

    # -------------------------------------------------------------------------
    # 4. Freeze provider/model in evaluateAdRemote
    # -------------------------------------------------------------------------
    old_remote = '''                // Gán đúng provider và model của provider đó
                payload.provider = selectedProvider;
                payload.model = (selectedProvider === 'openai')
                    ? (providerConfigs.openai.model || 'gpt-4o-mini')
                    : (providerConfigs.gemini.model || currentGeminiModel);'''

    new_remote = '''                // Snapshot bất biến: Không lấy trạng thái dropdown hiện tại ghi đè request đang chạy
                payload.provider = payload.provider || selectedProvider;
                payload.model = payload.model || ((payload.provider === 'openai')
                    ? (providerConfigs.openai.model || 'gpt-4o-mini')
                    : (providerConfigs.gemini.model || currentGeminiModel));'''

    if old_remote in html:
        html = html.replace(old_remote, new_remote)
        print("[APPLIED] evaluateAdRemote snapshot immutability fixed")

    # -------------------------------------------------------------------------
    # 5. Update Criteria A6 description
    # -------------------------------------------------------------------------
    old_a6 = '''                        id: 'crit_a6',
                        name: '6. Đủ thông tin bắt buộc theo luật',
                        desc: 'Bắt buộc ghi rõ tên thương nhân chịu trách nhiệm, xuất xứ, hạn sử dụng và dòng khuyến cáo pháp lý bắt buộc (Disclaimer).',
                        penalty: -15,'''

    new_a6 = '''                        id: 'crit_a6',
                        name: '6. Đủ thông tin bắt buộc theo luật',
                        desc: 'Bắt buộc công khai tên thương nhân, xuất xứ, điều kiện giấy phép hoạt động cơ sở theo ngành (Spa/thẩm mỹ: giấy phép; Mỹ phẩm: số công bố; TPBVSK: disclaimer bắt buộc). Lưu ý: Không thấy thông tin trong dữ liệu đọc khác với cơ sở không có giấy phép.',
                        penalty: -15,'''

    if old_a6 in html:
        html = html.replace(old_a6, new_a6)
        print("[APPLIED] Criteria A6 description updated with industry routing note")

    # -------------------------------------------------------------------------
    # 6. Add IdeaService.saveVariantAsIdea
    # -------------------------------------------------------------------------
    old_idea_ret = '''            return {
                init,
                filterByStatus,
                openAddModal,
                openEditModal,
                quickPushToProduction,
                renderProductionBoard,
                updateIdeaStage,
                toggleChecklistItem,
                saveProductionNotes,
                exportIdeas,
                importIdeas,
                deleteIdea,
                getIdeasList: () => JSON.parse(JSON.stringify(ideasList))
            };'''

    new_idea_ret = '''            function saveVariantAsIdea(variant, sessionTitle, brandName) {
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

            return {
                init,
                filterByStatus,
                openAddModal,
                openEditModal,
                quickPushToProduction,
                renderProductionBoard,
                updateIdeaStage,
                toggleChecklistItem,
                saveProductionNotes,
                exportIdeas,
                importIdeas,
                deleteIdea,
                saveVariantAsIdea,
                getIdeasList: () => JSON.parse(JSON.stringify(ideasList))
            };'''

    if old_idea_ret in html:
        html = html.replace(old_idea_ret, new_idea_ret)
        print("[APPLIED] IdeaService.saveVariantAsIdea added")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Stage 1 upgrade applied successfully.")

if __name__ == '__main__':
    apply_upgrade()
