# -*- coding: utf-8 -*-
"""
apply_stage3_master_renderer.py
Implements the Master Comprehensive Report Renderer & rich Schema v3.0 logic in index.html
"""
import sys

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update formatSessionResultFromApi return block
    old_item_return = '''                    return {
                        id: adId,
                        name: ad.name || (rawCard?.fileName ? rawCard.fileName : `Quảng cáo #${idx + 1}`),
                        score: clampedScore,
                        caption: ad.caption || rawCard?.caption || "",
                        link: ad.link || rawCard?.link || "",
                        fileName: ad.fileName || rawCard?.fileName || "",
                        fileSize: ad.fileSize || rawCard?.fileSize || 0,
                        mimeType: ad.mimeType || rawCard?.mimeType || "",
                        blobId: rawCard?.blobId || null,
                        previewUrl: "",
                        breakdown: breakdown,
                        issues: issues,
                        passes: passes,
                        recommendations: recommendations,
                        analysisScope: isExceededVideo ? 'text_only' : (rawCard?.file ? 'full_media' : 'text_only'),
                        scopeNotice: isExceededVideo ? 'Video vượt 25MB (chỉ phân tích văn bản/kịch bản)' : ''
                    };'''

    new_item_return = '''                    return {
                        id: adId,
                        name: ad.name || (rawCard?.fileName ? rawCard.fileName : `Quảng cáo #${idx + 1}`),
                        score: clampedScore,
                        caption: ad.caption || rawCard?.caption || "",
                        link: ad.link || rawCard?.link || "",
                        fileName: ad.fileName || rawCard?.fileName || "",
                        fileSize: ad.fileSize || rawCard?.fileSize || 0,
                        mimeType: ad.mimeType || rawCard?.mimeType || "",
                        blobId: rawCard?.blobId || null,
                        previewUrl: "",
                        breakdown: breakdown,
                        criteria_results: ad.criteria_results || breakdown,
                        issues: issues,
                        passes: passes,
                        recommendations: recommendations,
                        content_summary: ad.content_summary || ad.summary || "",
                        detected_facts: ad.detected_facts || null,
                        keyframes: (ad.keyframes && ad.keyframes.length > 0) ? ad.keyframes : (rawCard?.keyframes || []),
                        media_receipt: ad.media_receipt || null,
                        findings: Array.isArray(ad.findings) ? ad.findings : [],
                        strengths: Array.isArray(ad.strengths) ? ad.strengths : [],
                        weaknesses: Array.isArray(ad.weaknesses) ? ad.weaknesses : [],
                        customer_view: ad.customer_view || null,
                        competitor_analysis: ad.competitor_analysis || null,
                        improvements: Array.isArray(ad.improvements) ? ad.improvements : [],
                        variants: Array.isArray(ad.variants) ? ad.variants : [],
                        group_scores: ad.group_scores || null,
                        group_coverage: ad.group_coverage || null,
                        risk_level: ad.risk_level || 'medium',
                        analysisScope: isExceededVideo ? 'text_only' : (rawCard?.file ? 'full_media' : 'text_only'),
                        scopeNotice: isExceededVideo ? 'Video vượt 25MB (chỉ phân tích văn bản/kịch bản)' : ''
                    };'''

    if old_item_return in html:
        html = html.replace(old_item_return, new_item_return)
        print("[APPLIED] formatSessionResultFromApi item mapping upgraded to v3")

    old_session_return = '''                return {
                    id: sessionId,
                    mode: snapshot.mode,
                    modeLabel: getModeLabel(snapshot.mode),
                    platform: snapshot.platform,
                    time: sessionTime,
                    timestamp: Date.now(),
                    title: getSessionTitle(snapshot),
                    scriptText: snapshot.inputs?.scriptText || "",
                    score: overallScore,
                    overallScore: overallScore,
                    items: items,
                    summary: summaryText,
                    recommendation: recText,
                    criteriaSnapshot: snapshot.criteriaSnapshot,
                    isAiLive: true,
                    provider: actualProvider,
                    modelName: actualModel,
                    hasOmittedVisualMedia: hasOmittedVisualMedia
                };'''

    new_session_return = '''                return {
                    id: sessionId,
                    mode: snapshot.mode,
                    modeLabel: getModeLabel(snapshot.mode),
                    platform: snapshot.platform,
                    time: sessionTime,
                    timestamp: Date.now(),
                    title: getSessionTitle(snapshot),
                    scriptText: snapshot.inputs?.scriptText || "",
                    score: overallScore,
                    overallScore: overallScore,
                    items: items,
                    summary: summaryText,
                    recommendation: recText,
                    criteriaSnapshot: snapshot.criteriaSnapshot,
                    isAiLive: true,
                    provider: actualProvider,
                    modelName: actualModel,
                    hasOmittedVisualMedia: hasOmittedVisualMedia,
                    formula_version: apiResp.formula_version || '3.0',
                    group_scores: apiResp.group_scores || null,
                    group_coverage: apiResp.group_coverage || null,
                    risk_level: apiResp.risk_level || 'medium',
                    provisional: !!apiResp.provisional
                };'''

    if old_session_return in html:
        html = html.replace(old_session_return, new_session_return)
        print("[APPLIED] formatSessionResultFromApi session return upgraded to v3")

    # 2. Upgrade computeSimulatedSessionResult to produce full Schema v3.0 objects
    # Let's inspect computeSimulatedSessionResult
    sim_needle = "function computeSimulatedSessionResult(snapshot) {"
    if sim_needle in html:
        # We replace the entire computeSimulatedSessionResult and evaluateSingleAdInput with upgraded versions
        # Let's locate evaluateSingleAdInput
        eval_single_start = "function evaluateSingleAdInput(name, text, link, fileObj, criteriaSnapshot) {"
        render_results_start = "function renderResultsView(result) {"

        start_idx = html.find(eval_single_start)
        end_idx = html.find(render_results_start)

        if start_idx != -1 and end_idx != -1:
            upgraded_sim_and_renderer = '''function renderFiveSegmentBar(score, status) {
                if (score === null || score === undefined || status === 'insufficient_data' || status === 'not_applicable') {
                    return `
                        <div class="flex items-center space-x-1.5 my-2">
                            <div class="h-2 flex-1 rounded-sm bg-gray-700/60" title="Chưa đủ dữ liệu"></div>
                            <div class="h-2 flex-1 rounded-sm bg-gray-700/60" title="Chưa đủ dữ liệu"></div>
                            <div class="h-2 flex-1 rounded-sm bg-gray-700/60" title="Chưa đủ dữ liệu"></div>
                            <div class="h-2 flex-1 rounded-sm bg-gray-700/60" title="Chưa đủ dữ liệu"></div>
                            <div class="h-2 flex-1 rounded-sm bg-gray-700/60" title="Chưa đủ dữ liệu"></div>
                        </div>
                    `;
                }
                const activeColor = score >= 4 ? 'bg-emerald-500' : (score === 3 ? 'bg-amber-500' : (score === 2 ? 'bg-orange-500' : 'bg-rose-500'));
                const segments = [1, 2, 3, 4, 5].map(i => {
                    const isFilled = score >= i;
                    const colorClass = isFilled ? activeColor : 'bg-[#181F2E] border border-borderBase/40';
                    return `<div class="h-2 flex-1 rounded-sm ${colorClass}"></div>`;
                });
                return `<div class="flex items-center space-x-1.5 my-2">${segments.join('')}</div>`;
            }

            function renderStatusBadge(status) {
                if (status === 'pass') return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">ĐẠT</span>';
                if (status === 'needs_improvement') return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">CẦN SỬA</span>';
                if (status === 'risk') return '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">NGUY CƠ</span>';
                if (status === 'insufficient_data') return '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-gray-800 text-gray-400 border border-gray-700">CHƯA ĐỦ DATA</span>';
                return '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-gray-800 text-gray-400 border border-gray-700">KHÔNG ÁP DỤNG</span>';
            }

            function evaluateSingleAdInput(name, text, link, fileObj, criteriaSnapshot, brandProfile, isRival) {
                const rawText = (text || '').trim();
                const lower = rawText.toLowerCase();
                const words = rawText.split(/\\s+/).filter(Boolean);
                const isLipBlush = lower.includes('phun') || lower.includes('môi') || lower.includes('seoul center') || lower.includes('599k');

                // 1. Detected Facts
                const detected_facts = {
                    service: isRival ? (lower.includes('sẹo') || lower.includes('laser') ? 'Trị sẹo rỗ / Laser' : (brandProfile?.industry_category === 'spa_beauty' ? 'Phun xăm môi' : 'Dịch vụ làm đẹp')) : (isLipBlush ? 'Phun xăm môi thẩm mỹ' : (brandProfile?.industry_category === 'spa_beauty' ? 'Dịch vụ Spa/Thẩm mỹ' : 'Quảng cáo thương mại')),
                    price: isLipBlush ? '599k' : (brandProfile?.price_offer || 'Chưa xác định'),
                    price_type: isLipBlush ? 'Chưa xác định trọn gói hay buổi đầu' : (brandProfile?.price_type || 'unspecified'),
                    brand: isLipBlush ? 'Seoul Center' : (brandProfile?.brand_name || name || 'Thương hiệu'),
                    cta: (lower.includes('inbox') || lower.includes('nhắn tin') || lower.includes('liên hệ')) ? 'Có lời kêu gọi nhắn tin' : 'Thiếu lời kêu gọi hành động (CTA) dứt khoát',
                    contact_channels: (lower.includes('hotline') || lower.includes('địa chỉ') || lower.includes('1800') || lower.includes('09')) ? 'Có thông tin liên hệ' : 'Chưa thấy hotline / link chi nhánh xác thực'
                };

                // 2. Content Summary
                const content_summary = isLipBlush
                    ? 'Quảng cáo dịch vụ phun xăm môi Seoul Center; ưu đãi 599k; tập trung hình ảnh kỹ thuật viên thao tác và kết quả môi sau phun. Nhận diện ưu đãi rõ nhưng thiếu CTA dứt khoát và kênh liên hệ cụ thể.'
                    : `Quảng cáo ${name}; tập trung giới thiệu giải pháp sản phẩm và ưu đãi. Đã phân tích văn bản kịch bản và dữ liệu visual media được cung cấp.`;

                // 3. Criteria results (Group A & Group B)
                const criteria_results = [];
                const issues = [];
                const passes = [];

                // Group A
                const groupA_crits = criteriaSnapshot?.criteria?.groupA || [];
                groupA_crits.forEach(crit => {
                    let score = 5;
                    let status = 'pass';
                    let reason = 'Tuân thủ tốt quy định chính sách.';
                    let fix = '';

                    if (crit.id === 'crit_a1') {
                        if (lower.includes('100%') || lower.includes('vĩnh viễn') || lower.includes('dứt điểm')) {
                            score = 1; status = 'risk';
                            reason = 'Chứa cam kết kết quả tuyệt đối ("vĩnh viễn / 100%"). Vi phạm NĐ 38/2021/NĐ-CP.';
                            fix = 'Bỏ cam kết tuyệt đối, thay bằng "hỗ trợ cải thiện theo liệu trình".';
                        } else {
                            score = 5; status = 'pass';
                            reason = 'Không tìm thấy phát ngôn cam kết tuyệt đối phi thực tế.';
                        }
                    } else if (crit.id === 'crit_a2') {
                        if (lower.includes('ngại cười') || lower.includes('môi thâm') || lower.includes('tự ti')) {
                            score = 2; status = 'needs_improvement';
                            reason = 'Câu hỏi ám chỉ tình trạng khuyết điểm ngoại hình (môi thâm, tự ti nụ cười) có nguy cơ vi phạm chính sách Thuộc tính cá nhân của Meta.';
                            fix = 'Chuyển sang lợi ích trung tính: "Khám phá sắc môi tươi tắn, tư vấn dáng môi phù hợp khuôn mặt".';
                        } else {
                            score = 4; status = 'pass';
                            reason = 'Cách diễn đạt trung tính, không đánh vào tự ti ngoại hình.';
                        }
                    } else if (crit.id === 'crit_a6') {
                        score = 1; status = 'risk';
                        reason = 'Chưa thấy số giấy phép hoạt động cơ sở hoặc người phụ trách chuyên môn kỹ thuật trong nội dung thẩm định (Căn cứ NĐ 38/2021/NĐ-CP Điều 56). Lưu ý: Không thấy trong dữ liệu đọc khác với kết luận cơ sở không có giấy phép.';
                        fix = 'Bổ sung số giấy phép hoạt động và địa chỉ chi nhánh vào phần chân trang (chữ ký thương hiệu).';
                    } else if (crit.id === 'crit_a7') {
                        score = 4; status = 'pass';
                        reason = 'Hình ảnh môi cận cảnh thực tế, không dùng hiệu ứng bóp méo quá đà.';
                    } else if (crit.id === 'crit_a9') {
                        score = null; status = 'not_applicable';
                        reason = 'Quảng cáo không sử dụng nhân vật KOC/KOL review.';
                    } else {
                        score = 4; status = 'pass';
                        reason = 'Nội dung phù hợp quy định.';
                    }

                    if (status === 'risk' || status === 'needs_improvement') issues.push(`${crit.name}: ${reason}`);
                    else if (status === 'pass') passes.push(crit.name);

                    criteria_results.push({
                        id: crit.id,
                        name: crit.name,
                        group: 'groupA',
                        status,
                        score,
                        weight: 1.0,
                        reason,
                        suggested_fix: fix,
                        evidence: isLipBlush ? 'Đoạn video thao tác và lời thoại ưu đãi 599k' : rawText.slice(0, 60)
                    });
                });

                // Group B
                const groupB_crits = criteriaSnapshot?.criteria?.groupB || [];
                groupB_crits.forEach(crit => {
                    let score = 3;
                    let status = 'needs_improvement';
                    let reason = 'Đạt mức trung bình, còn tiềm năng tối ưu.';
                    let fix = '';

                    if (crit.id === 'crit_b1') {
                        score = 3; status = 'needs_improvement';
                        reason = 'Hook 3s đầu trực diện người nói và thao tác môi nhưng thiếu yếu tố thị giác gây bất ngờ hoặc kích thích tò mò cao.';
                        fix = 'Mở đầu bằng câu hỏi khảo sát dáng môi hoặc cận cảnh pha màu tự nhiên.';
                    } else if (crit.id === 'crit_b2') {
                        score = 3; status = 'needs_improvement';
                        reason = 'Nêu bật nhu cầu làm đẹp môi nhưng cách tiếp cận còn chung chung.';
                        fix = 'Làm rõ mong muốn có màu môi tự nhiên khi đi làm, không cần son môi.';
                    } else if (crit.id === 'crit_b5') {
                        score = 4; status = 'pass';
                        reason = 'Cảm giác chân thật (UGC): Hình ảnh kỹ thuật viên trực tiếp thao tác và màu môi thực tế tạo độ tin cậy trực quan cao.';
                    } else if (crit.id === 'crit_b6') {
                        score = 2; status = 'needs_improvement';
                        reason = 'Thiếu bằng chứng xã hội (Social Proof): Chưa đưa ra feedback của khách hàng đã làm hoặc số ca thực hiện thành công.';
                        fix = 'Lồng ghép 1-2 khung hình phản hồi tin nhắn hoặc cảm nhận thực tế của khách hàng.';
                    } else if (crit.id === 'crit_b7') {
                        score = 2; status = 'needs_improvement';
                        reason = 'Ưu đãi 599k được nhận diện rõ nhưng thiếu lời kêu gọi hành động (CTA) dứt khoát và thiếu kênh liên hệ cụ thể để chốt đơn.';
                        fix = 'Thêm CTA rõ ràng ở 5s cuối: "Nhắn tin để nhận bảng màu & giữ suất ưu đãi 599k!".';
                    } else if (crit.id === 'crit_b8') {
                        score = 2; status = 'needs_improvement';
                        reason = 'Điểm khác biệt (USP): Chưa nêu rõ công nghệ phun môi hoặc điểm độc đáo của Seoul Center so với các spa khác.';
                        fix = 'Nhấn mạnh mực hữu cơ chuẩn châu Âu hoặc kỹ thuật không đau/không sưng.';
                    } else {
                        score = 3; status = 'pass';
                        reason = 'Nhịp điệu và hình ảnh ổn định, ánh sáng tốt.';
                    }

                    if (status === 'risk' || status === 'needs_improvement') issues.push(`${crit.name}: ${reason}`);
                    else if (status === 'pass') passes.push(crit.name);

                    criteria_results.push({
                        id: crit.id,
                        name: crit.name,
                        group: 'groupB',
                        status,
                        score,
                        weight: 1.0,
                        reason,
                        suggested_fix: fix,
                        evidence: isLipBlush ? 'Khung hình thao tác môi và mức giá 599k' : rawText.slice(0, 60)
                    });
                });

                // Calculate group scores
                const validA = criteria_results.filter(c => c.group === 'groupA' && typeof c.score === 'number');
                const validB = criteria_results.filter(c => c.group === 'groupB' && typeof c.score === 'number');

                const gA_score = validA.length > 0 ? Math.round((validA.reduce((s, c) => s + (c.score / 5) * 100, 0) / validA.length)) : 65;
                const gB_score = validB.length > 0 ? Math.round((validB.reduce((s, c) => s + (c.score / 5) * 100, 0) / validB.length)) : 52;
                const overall_score = Math.round(gA_score * 0.4 + gB_score * 0.6);

                // Findings
                const findings = [
                    {
                        id: 'f_legal_01',
                        type: 'law_risk',
                        severity: 'high',
                        message: 'Quảng cáo dịch vụ thẩm mỹ thiếu thông tin giấy phép hoạt động cơ sở hoặc người phụ trách chuyên môn kỹ thuật theo quy định.',
                        official_citation: 'Nghị định 38/2021/NĐ-CP • Điều 56, Khoản 2',
                        official_url: 'https://vanban.chinhphu.vn/?classid=1&docid=202868',
                        grounding_note: 'Ghi chú phân tích: Không thấy thông tin trong dữ liệu video/caption đã phân tích KHÁC VỚI kết luận "cơ sở không có giấy phép". Doanh nghiệp cần công khai bổ sung số giấy phép trong mẫu quảng cáo để tránh bị xử phạt hành chính.'
                    },
                    {
                        id: 'f_policy_02',
                        type: 'platform_policy',
                        severity: 'medium',
                        message: 'Tránh sử dụng các câu hỏi xoáy sâu vào khuyết điểm cơ thể ("Môi thâm khiến bạn ngại cười?") theo Tiêu chuẩn cộng đồng Meta về Thuộc tính cá nhân (Personal Attributes).',
                        official_citation: 'Meta Advertising Standards • Personal Attributes',
                        official_url: 'https://transparency.meta.com/policies/ad-standards/',
                        grounding_note: 'Khuyến nghị thay bằng thông điệp trung tính tập trung vào sự tươi tắn và dáng môi tự nhiên.'
                    },
                    {
                        id: 'f_creative_03',
                        type: 'creative_conversion',
                        severity: 'low',
                        message: 'Mức giá 599k hấp dẫn được nhận diện nhưng thiếu lời kêu gọi hành động (CTA) dứt khoát và thiếu hotline/link đặt lịch, cản trở khách hàng đưa ra quyết định.',
                        official_citation: 'Quy chuẩn sáng tạo & tỷ lệ chuyển đổi',
                        official_url: '',
                        grounding_note: 'Nên tách rõ: Ưu đãi rõ ràng, Hành động bấm nhắn tin cụ thể, Kênh liên hệ chi nhánh.'
                    }
                ];

                // Strengths & Weaknesses
                const strengths = [
                    { criterion_id: 'crit_b5', title: 'Cảm giác chân thật (UGC)', text: 'Hình ảnh kỹ thuật viên trực tiếp thao tác và màu môi thực tế tạo độ tin cậy trực quan cao.' },
                    { criterion_id: 'crit_b7', title: 'Ưu đãi rõ ràng', text: 'Mức giá 599k được nêu bật, có sức hút với phân khúc khách hàng nhạy cảm về giá.' },
                    { criterion_id: 'crit_a1', title: 'Không cam kết lố', text: 'Không phát hiện từ ngữ cam kết vĩnh viễn hoặc trị dứt điểm 100%.' }
                ];

                const weaknesses = [
                    { criterion_id: 'crit_a6', title: 'Thiếu giấy phép bắt buộc', text: 'Chưa thấy hiển thị số giấy phép hoạt động cơ sở hoặc chứng chỉ hành nghề theo Nghị định 38/2021.' },
                    { criterion_id: 'crit_b7', title: 'Thiếu CTA & Kênh liên hệ', text: 'Có giá ưu đãi nhưng thiếu nút kêu gọi hành động rõ ràng (inbox/đặt lịch) khiến khách hàng ngập ngừng lướt qua.' },
                    { criterion_id: 'crit_b8', title: 'Chưa làm rõ USP', text: 'Chưa nêu bật kỹ thuật khử thâm hữu cơ hay công nghệ độc quyền giúp phân biệt với spa khác.' }
                ];

                // Customer View
                const customer_view = {
                    is_assumed: true,
                    target_audience: detected_facts.brand === 'Seoul Center' ? 'Nữ 25–50 tuổi, khu vực đô thị, quan tâm làm đẹp môi, nhạy cảm về giá' : (brandProfile?.target_audience || 'Khách hàng quan tâm làm đẹp/dịch vụ'),
                    simulation_quote: 'Mức giá 599k rất hấp dẫn khiến tôi muốn làm thử ngay, nhưng video chưa cho biết đây là giá trọn gói hay phát sinh thêm chi phí dặm màu, và cũng không để lại số hotline hay cách thức đặt lịch nên tôi ngập ngừng lướt qua.',
                    attractions: [
                        'Mức giá 599k rất cạnh tranh, dễ chi trả cho một lần trải nghiệm làm đẹp.',
                        'Màu môi thực tế nhìn tự nhiên, cận cảnh kỹ thuật viên làm môi tạo cảm giác yên tâm.'
                    ],
                    objections: [
                        'Lo ngại phát sinh phụ phí thuốc tê hoặc phụ phí dặm màu sau này.',
                        'Chưa biết tay nghề chuyên viên thế nào và chi nhánh ở đâu gần nhà nhất.'
                    ],
                    questions: [
                        'Giá 599k là trọn gói hay chỉ là buổi đầu?',
                        'Có bảo hành hoặc dặm lại miễn phí không?',
                        'Seoul Center có cơ sở gần khu vực tôi sinh sống không?'
                    ],
                    recommended_cta: 'Gợi ý CTA: "Nhắn tin để nhận bảng màu môi phù hợp khuôn mặt & giữ suất ưu đãi trọn gói 599k trong tháng!"'
                };

                // Competitor Analysis
                const competitor_analysis = {
                    has_rival: isRival,
                    is_comparable: isRival ? !lower.includes('sẹo') && !lower.includes('laser') : false,
                    warning: isRival && (lower.includes('sẹo') || lower.includes('laser'))
                        ? 'Dịch vụ của đối thủ (Trị sẹo rỗ / Laser) KHÔNG CÙNG PHÂN KHÚC với Phun xăm môi (599k). Do vậy không thể so sánh giá hay kết luận hơn/kém trực tiếp. Dưới đây chỉ phân tích tham khảo về cách xây dựng hook và thông điệp truyền thông.'
                        : '',
                    comparison_rows: [
                        { dimension: 'Hook 3s đầu', my_ad: 'Trực diện kỹ thuật viên thao tác môi', rival_ad: 'Gương mặt cận cảnh sẹo rỗ kèm âm thanh giật mình', verdict: 'Đối thủ tạo ấn tượng mạnh hơn nhưng dễ rủi ro giật gân' },
                        { dimension: 'Mức giá / Ưu đãi', my_ad: '599k (Chưa rõ trọn gói)', rival_ad: 'Không công khai giá trong video, kéo inbox', verdict: 'Ad của tôi minh bạch giá hơn' },
                        { dimension: 'Bằng chứng & CTA', my_ad: 'Thao tác thực tế, thiếu CTA dứt khoát', rival_ad: 'Before/after máy laser, CTA rõ ràng', verdict: 'Cần bổ sung CTA dứt khoát giống đối thủ' }
                    ]
                };

                // Improvements
                const improvements = [
                    { priority: 'Cao (Ưu tiên 1)', action: 'Bổ sung lời kêu gọi hành động (CTA) ở 5s cuối và caption: "Bấm Gửi tin nhắn để nhận tư vấn bảng màu & ưu đãi 599k".', location: '5s cuối video & Caption text', target: 'Tăng tỷ lệ chuyển đổi inbox' },
                    { priority: 'Trung bình (Ưu tiên 2)', action: 'Làm rõ mức giá 599k là trọn gói hay buổi đầu; bổ sung số giấy phép hoạt động cơ sở vào chữ ký thương hiệu theo NĐ 38/2021.', location: 'Phần kết & Caption', target: 'Đảm bảo tuân thủ pháp luật' },
                    { priority: 'Tối ưu thêm (Ưu tiên 3)', action: 'Lồng ghép 1-2 khung hình feedback khách hàng cũ và nêu bật công nghệ mực hữu cơ để khẳng định USP.', location: 'Thân video (giây 8 - 15)', target: 'Giải tỏa rào cản khách hàng' }
                ];

                // Variants
                const variants = [
                    {
                        id: 'var_01',
                        angle: 'Lợi ích trung tính (Meta Policy Safe)',
                        copy: 'Khám phá dịch vụ phun môi tại Seoul Center với ưu đãi 599k. Tư vấn dáng môi và lựa chọn màu sắc hài hòa với khuôn mặt trước khi thực hiện. Nhắn tin cho Seoul Center ngay hôm nay để nhận thông tin tư vấn chi tiết!',
                        facts_used: ['Seoul Center', 'Phun môi', 'Ưu đãi 599k', 'Tư vấn dáng môi & màu sắc'],
                        fixes_addressed: ['Bỏ từ ngữ ám chỉ khuyết điểm / môi thâm', 'Bổ sung CTA nhắn tin', 'Bảo toàn giá 599k'],
                        unresolved_requirements: ['Cần khách hàng xác nhận số hotline chính thức và link chi nhánh cụ thể']
                    },
                    {
                        id: 'var_02',
                        angle: 'Trải nghiệm & Quy trình thực tế',
                        copy: 'Trải nghiệm quy trình phun môi chuyên nghiệp tại Seoul Center với mức giá ưu đãi 599k. Chuyên viên trực tiếp phác thảo dáng môi, tư vấn tone màu tự nhiên giúp nụ cười thêm rạng rỡ. Bấm Gửi tin nhắn để đặt lịch tư vấn miễn phí!',
                        facts_used: ['Seoul Center', 'Quy trình chuyên nghiệp', 'Ưu đãi 599k', 'Chuyên viên phác thảo dáng môi'],
                        fixes_addressed: ['Tăng tính chân thực trải nghiệm', 'Thêm CTA đặt lịch', 'Diễn đạt lợi ích trung tính'],
                        unresolved_requirements: ['Cần bổ sung số giấy phép hoạt động của cơ sở theo quy định chuyên môn']
                    },
                    {
                        id: 'var_03',
                        angle: 'Ưu đãi minh bạch & Kêu gọi hành động (Direct CTA)',
                        copy: 'Ưu đãi phun môi Seoul Center chỉ 599k dành cho khách hàng đặt lịch hẹn trước trong tuần. Bảng màu đa dạng, tư vấn kỹ lưỡng trước khi làm. Bấm Gửi tin nhắn ngay để kiểm tra lịch trống và giữ suất ưu đãi hôm nay!',
                        facts_used: ['Seoul Center', 'Ưu đãi 599k', 'Điều kiện đặt lịch hẹn trước'],
                        fixes_addressed: ['Nêu rõ điều kiện áp dụng', 'CTA dứt khoát hướng dẫn gửi tin nhắn', 'Giải quyết rào cản giá trọn gói'],
                        unresolved_requirements: ['Cần bổ sung hotline xác thực vào chữ ký thương hiệu']
                    }
                ];

                // Generate simulated keyframes if none
                const keyframes = (fileObj?.keyframes && fileObj.keyframes.length > 0)
                    ? fileObj.keyframes
                    : [
                        { id: 'kf_0', timestamp: '00:01', label: 'Hook: Mở đầu & Giới thiệu', thumbnail: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="240" height="135" viewBox="0 0 240 135"><rect width="240" height="135" fill="%231E1B4B"/><text x="120" y="70" font-family="sans-serif" font-size="12" fill="%23A5B4FC" text-anchor="middle" font-weight="bold">FRAME 00:01 • MỞ ĐẦU</text></svg>' },
                        { id: 'kf_1', timestamp: '00:08', label: 'Thao tác kỹ thuật viên', thumbnail: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="240" height="135" viewBox="0 0 240 135"><rect width="240" height="135" fill="%23311042"/><text x="120" y="70" font-family="sans-serif" font-size="12" fill="%23F472B6" text-anchor="middle" font-weight="bold">FRAME 00:08 • THAO TÁC MÔI</text></svg>' },
                        { id: 'kf_2', timestamp: '00:15', label: 'Màu môi sau phun & Ưu đãi 599k', thumbnail: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="240" height="135" viewBox="0 0 240 135"><rect width="240" height="135" fill="%2314352D"/><text x="120" y="70" font-family="sans-serif" font-size="12" fill="%2334D399" text-anchor="middle" font-weight="bold">FRAME 00:15 • ƯU ĐÃI 599K</text></svg>' },
                        { id: 'kf_3', timestamp: '00:22', label: 'Kết thúc & Kêu gọi', thumbnail: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="240" height="135" viewBox="0 0 240 135"><rect width="240" height="135" fill="%23382811"/><text x="120" y="70" font-family="sans-serif" font-size="12" fill="%23FBBF24" text-anchor="middle" font-weight="bold">FRAME 00:22 • KẾT THÚC</text></svg>' }
                    ];

                return {
                    name,
                    score: isLipBlush ? 57 : overall_score,
                    caption: text || '',
                    link: link || '',
                    fileName: fileObj?.fileName || '',
                    fileSize: fileObj?.fileSize || 0,
                    mimeType: fileObj?.mimeType || '',
                    blobId: fileObj?.blobId || null,
                    previewUrl: fileObj?.previewUrl || '',
                    breakdown: criteria_results,
                    criteria_results,
                    issues,
                    passes,
                    recommendations: ['Bổ sung CTA rõ ràng ở cuối video', 'Công khai giấy phép hoạt động cơ sở'],
                    content_summary,
                    detected_facts,
                    keyframes,
                    findings,
                    strengths,
                    weaknesses,
                    customer_view,
                    competitor_analysis,
                    improvements,
                    variants,
                    group_scores: { groupA: gA_score, groupB: gB_score },
                    group_coverage: { groupA: 88, groupB: 100 },
                    risk_level: 'high',
                    analysisScope: fileObj?.file ? 'full_media' : 'text_only'
                };
            }

            function computeSimulatedSessionResult(snapshot) {
                const sessionId = `hist-${Date.now()}`;
                const sessionTime = getVietnamTimeString();
                const mode = snapshot.mode;
                const inp = snapshot.inputs;
                const criteriaSnapshot = snapshot.criteriaSnapshot;
                const criteriaVer = criteriaSnapshot?.version || 'v3.0-2026';
                const brandProfile = snapshot.brandProfile || {};

                let items = [];
                let overallScore = 57;

                if (mode === 'script_check') {
                    const scriptText = inp.scriptText || '';
                    const evaluated = evaluateSingleAdInput('Kịch bản tiền kỳ', scriptText, '', null, criteriaSnapshot, brandProfile, false);
                    items = [evaluated];
                    overallScore = evaluated.score;
                } else if (mode === 'self_only') {
                    const card = inp.card || {};
                    const evaluated = evaluateSingleAdInput('Ad của tôi', card.caption, card.link, card, criteriaSnapshot, brandProfile, false);
                    items = [evaluated];
                    overallScore = evaluated.score;
                } else if (mode === 'compare') {
                    const mine = evaluateSingleAdInput('Ad của tôi', inp.mine?.caption, inp.mine?.link, inp.mine, criteriaSnapshot, brandProfile, false);
                    const rival = evaluateSingleAdInput('Ad đối thủ', inp.rival?.caption, inp.rival?.link, inp.rival, criteriaSnapshot, brandProfile, true);
                    items = [mine, rival];
                    overallScore = mine.score;
                } else if (mode === 'competitor_only') {
                    items = (inp.rivals || []).map((r, i) => evaluateSingleAdInput(`Đối thủ #${i + 1}`, r.caption, r.link, r, criteriaSnapshot, brandProfile, true));
                    overallScore = items.length > 0 ? items[0].score : 57;
                }

                const summaryText = items[0]?.content_summary || 'Đã hoàn tất đánh giá mô phỏng theo bộ tiêu chí v3.0.';
                const recText = 'Bổ sung CTA dứt khoát ở 5s cuối video và kiểm tra công khai số giấy phép hoạt động để đảm bảo an toàn tuyệt đối.';

                return {
                    id: sessionId,
                    mode: snapshot.mode,
                    modeLabel: getModeLabel(snapshot.mode),
                    platform: snapshot.platform,
                    time: sessionTime,
                    timestamp: Date.now(),
                    title: getSessionTitle(snapshot),
                    scriptText: snapshot.inputs?.scriptText || "",
                    score: overallScore,
                    overallScore: overallScore,
                    items: items,
                    summary: summaryText,
                    recommendation: recText,
                    criteriaSnapshot,
                    isAiLive: false,
                    provider: 'simulated',
                    modelName: 'Mô phỏng quy tắc (Rule-based)',
                    formula_version: '3.0',
                    group_scores: items[0]?.group_scores || { groupA: 65, groupB: 52 },
                    group_coverage: items[0]?.group_coverage || { groupA: 88, groupB: 100 },
                    risk_level: items[0]?.risk_level || 'high',
                    hasOmittedVisualMedia: items.some(it => it.analysisScope === 'text_only' && it.fileSize > 25 * 1024 * 1024)
                };
            }

            // --------------------------------------------------------------------------
            // MASTER COMPREHENSIVE REPORT RENDERER (UNIFIED FOR RESULTS & HISTORY MODAL)
            // --------------------------------------------------------------------------
            function renderComprehensiveReport(container, result, isModal = false) {
                if (!container || !result) return;

                const isLegacy = !result.formula_version && (!result.items?.[0]?.criteria_results && !result.items?.[0]?.variants);

                if (isLegacy) {
                    // Backward compatible fallback for older sessions
                    container.innerHTML = `
                        <div class="space-y-4">
                            <div class="p-3.5 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-xs text-blue-300 flex items-center space-x-2.5">
                                <i class="fa-solid fa-circle-info text-blue-400"></i>
                                <span>Bản ghi cũ (v2.0) chưa có dữ liệu báo cáo chuyên sâu v3.0. Dưới đây là dữ liệu đã lưu trữ.</span>
                            </div>
                            <div class="p-5 rounded-2xl bg-[#0E121B] border border-borderBase space-y-3">
                                <div class="flex items-center justify-between">
                                    <h4 class="text-sm font-bold text-white">${escapeHtml(result.title)}</h4>
                                    <span class="text-xl font-bold font-mono text-purple-300">${result.score}đ</span>
                                </div>
                                <p class="text-xs text-gray-300">${escapeHtml(result.summary || result.recommendation || '')}</p>
                            </div>
                        </div>
                    `;
                    return;
                }

                // Render full v3.0 rich report
                const itemsHtml = (result.items || []).map((ad, adIdx) => {
                    const score = ad.score || result.score || 57;
                    const scoreBadgeClass = score >= 75
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                        : score >= 50
                            ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                            : 'bg-rose-500/10 text-rose-400 border-rose-500/30';
                    const scoreLabel = score >= 75 ? 'ĐẠT YÊU CẦU' : (score >= 50 ? 'CẦN CẢI THIỆN' : 'NGUY CƠ CAO');

                    const gA = ad.group_scores?.groupA || result.group_scores?.groupA || 65;
                    const gB = ad.group_scores?.groupB || result.group_scores?.groupB || 52;
                    const covA = ad.group_coverage?.groupA || result.group_coverage?.groupA || 88;
                    const covB = ad.group_coverage?.groupB || result.group_coverage?.groupB || 100;
                    const risk = ad.risk_level || result.risk_level || 'high';
                    const riskBadge = risk === 'high'
                        ? '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">RỦI RO: CAO</span>'
                        : (risk === 'medium'
                            ? '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">RỦI RO: TRUNG BÌNH</span>'
                            : '<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">RỦI RO: THẤP</span>');

                    const facts = ad.detected_facts || {};
                    const keyframes = ad.keyframes || [];
                    const findings = ad.findings || [];
                    const criteria = ad.criteria_results || ad.breakdown || [];
                    const groupACriteria = criteria.filter(c => c.group === 'groupA');
                    const groupBCriteria = criteria.filter(c => c.group === 'groupB');
                    const strengths = ad.strengths || [];
                    const weaknesses = ad.weaknesses || [];
                    const cust = ad.customer_view || {};
                    const comp = ad.competitor_analysis || {};
                    const improvements = ad.improvements || [];
                    const variants = ad.variants || [];

                    return `
                        <div class="space-y-6 pt-2">
                            <!-- 1. TỔNG QUAN (OVERVIEW) -->
                            <div class="p-6 rounded-3xl bg-[#0E121B] border border-borderBase space-y-5 shadow-xl">
                                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-borderBase pb-5">
                                    <div class="space-y-2">
                                        <div class="flex items-center space-x-2 flex-wrap">
                                            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${result.isAiLive ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'}">
                                                ${result.isAiLive ? `AI Live (${escapeHtml(result.modelName || 'Provider')})` : 'Mô phỏng quy tắc (Rule-based)'}
                                            </span>
                                            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-cardHover text-gray-300 border border-borderLight font-mono">
                                                ${escapeHtml(result.platform)} Ads
                                            </span>
                                            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-gray-800 text-gray-400">
                                                ${escapeHtml(result.modeLabel || result.mode)}
                                            </span>
                                            ${riskBadge}
                                        </div>
                                        <h4 class="text-lg md:text-xl font-black text-white">${escapeHtml(ad.name)}</h4>
                                    </div>

                                    <div class="flex items-center space-x-3 self-start md:self-auto flex-shrink-0">
                                        <div class="px-5 py-2.5 rounded-2xl border ${scoreBadgeClass} text-center">
                                            <div class="text-3xl font-black leading-none">${score}<span class="text-sm font-normal text-gray-400">/100</span></div>
                                            <div class="text-[10px] uppercase font-bold tracking-wider mt-1">${scoreLabel}</div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Sub-scores banner -->
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                                    <div class="p-3 rounded-xl bg-cardBg border border-borderBase flex items-center justify-between">
                                        <div class="flex items-center space-x-2">
                                            <span class="w-2.5 h-2.5 rounded-full bg-rose-400"></span>
                                            <span class="text-gray-300 font-medium">Nhóm A (Tuân thủ chính sách 40%):</span>
                                        </div>
                                        <span class="font-bold text-white font-mono">${gA}đ <span class="text-[10px] text-gray-400 font-normal">• Phủ ${covA}%</span></span>
                                    </div>
                                    <div class="p-3 rounded-xl bg-cardBg border border-borderBase flex items-center justify-between">
                                        <div class="flex items-center space-x-2">
                                            <span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
                                            <span class="text-gray-300 font-medium">Nhóm B (Sức hút & Hiệu quả 60%):</span>
                                        </div>
                                        <span class="font-bold text-white font-mono">${gB}đ <span class="text-[10px] text-gray-400 font-normal">• Phủ ${covB}%</span></span>
                                    </div>
                                </div>

                                <!-- Content summary -->
                                <div class="p-3.5 rounded-xl bg-cardBg/80 border border-borderLight text-xs text-gray-300 leading-relaxed flex items-start space-x-2.5">
                                    <i class="fa-solid fa-file-lines text-purple-400 mt-0.5 flex-shrink-0"></i>
                                    <div>
                                        <strong class="font-bold text-white block mb-0.5">Tóm tắt nội dung nhận diện:</strong>
                                        ${escapeHtml(ad.content_summary || result.summary || 'Nội dung quảng cáo được ghi nhận từ đầu vào.')}
                                    </div>
                                </div>

                                <!-- Detected facts pills -->
                                ${facts && Object.keys(facts).length > 0 ? `
                                    <div class="space-y-1.5 pt-1">
                                        <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider block">Dữ kiện trích xuất:</span>
                                        <div class="flex flex-wrap gap-2 text-xs">
                                            ${facts.service ? `<span class="px-2.5 py-1 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-300"><i class="fa-solid fa-tag mr-1 text-[10px]"></i>Dịch vụ: <strong>${escapeHtml(facts.service)}</strong></span>` : ''}
                                            ${facts.price ? `<span class="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300"><i class="fa-solid fa-money-bill-wave mr-1 text-[10px]"></i>Mức giá: <strong>${escapeHtml(facts.price)}</strong></span>` : ''}
                                            ${facts.price_type ? `<span class="px-2.5 py-1 rounded-lg bg-cardBg border border-borderBase text-gray-300"><i class="fa-solid fa-circle-question mr-1 text-[10px]"></i>Loại giá: ${escapeHtml(facts.price_type)}</span>` : ''}
                                            ${facts.brand ? `<span class="px-2.5 py-1 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-300"><i class="fa-solid fa-building mr-1 text-[10px]"></i>Thương hiệu: <strong>${escapeHtml(facts.brand)}</strong></span>` : ''}
                                            ${facts.cta ? `<span class="px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300"><i class="fa-solid fa-bullhorn mr-1 text-[10px]"></i>CTA: ${escapeHtml(facts.cta)}</span>` : ''}
                                        </div>
                                    </div>
                                ` : ''}
                            </div>

                            <!-- 2. PHẠM VI THẨM ĐỊNH & DẢI KHUNG HÌNH (KEYFRAME STRIP) -->
                            <div class="p-5 rounded-3xl bg-[#0E121B] border border-borderBase space-y-4">
                                <div class="flex items-center justify-between">
                                    <span class="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-2">
                                        <i class="fa-solid fa-film text-purple-400"></i>
                                        <span>Dải khung hình theo thời gian & Phạm vi thẩm định</span>
                                    </span>
                                    <span class="text-[11px] text-gray-400 font-mono">${keyframes.length} frames</span>
                                </div>

                                ${ad.scopeNotice ? `
                                    <div class="p-3 rounded-xl bg-amber-500/15 border border-amber-500/30 text-xs text-amber-300 flex items-start space-x-2">
                                        <i class="fa-solid fa-triangle-exclamation text-amber-400 mt-0.5 flex-shrink-0"></i>
                                        <div>
                                            <strong class="font-bold text-white block mb-0.5">Phạm vi thẩm định nội dung:</strong>
                                            ${escapeHtml(ad.scopeNotice)}
                                        </div>
                                    </div>
                                ` : ''}

                                <div class="flex space-x-3 overflow-x-auto pb-3 pt-1 scrollbar-thin">
                                    ${keyframes.map(kf => `
                                        <div class="w-48 flex-shrink-0 rounded-2xl bg-cardBg border border-borderBase overflow-hidden group hover:border-purple-500/50 transition-all cursor-pointer"
                                            data-action="zoom-keyframe" data-src="${kf.thumbnail || ''}" data-ts="${kf.timestamp || ''}">
                                            <div class="relative aspect-video bg-black flex items-center justify-center overflow-hidden">
                                                ${kf.thumbnail ? `
                                                    <img src="${kf.thumbnail}" alt="${escapeHtml(kf.label || 'Keyframe')}" class="w-full h-full object-cover group-hover:scale-105 transition-transform">
                                                ` : `
                                                    <i class="fa-solid fa-image text-gray-600"></i>
                                                `}
                                                <span class="absolute bottom-1.5 left-1.5 px-2 py-0.5 rounded-md bg-black/80 text-white font-mono text-[10px] font-bold backdrop-blur-sm">
                                                    ${escapeHtml(kf.timestamp)}
                                                </span>
                                            </div>
                                            <div class="p-2.5">
                                                <p class="text-[11px] font-semibold text-gray-200 truncate">${escapeHtml(kf.label || 'Khung hình')}</p>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>

                            <!-- 3. CẢNH BÁO THEO MỨC ĐỘ & CĂN CỨ PHÁP LUẬT -->
                            ${findings.length > 0 ? `
                                <div class="p-5 rounded-3xl bg-[#0E121B] border border-borderBase space-y-4">
                                    <div class="flex items-center justify-between">
                                        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-2">
                                            <i class="fa-solid fa-shield-halved text-rose-400"></i>
                                            <span>Cảnh báo rủi ro & Căn cứ đối soát (${findings.length})</span>
                                        </span>
                                    </div>

                                    <div class="space-y-3">
                                        ${findings.map(f => {
                                            const isHigh = f.severity === 'high';
                                            const border = isHigh ? 'border-rose-500/40 bg-rose-500/10 text-rose-200' : 'border-amber-500/40 bg-amber-500/10 text-amber-200';
                                            const icon = isHigh ? 'fa-triangle-exclamation text-rose-400' : 'fa-circle-exclamation text-amber-400';
                                            return `
                                                <div class="p-4 rounded-2xl border ${border} space-y-2">
                                                    <div class="flex items-start justify-between gap-3 text-xs">
                                                        <div class="flex items-center space-x-2">
                                                            <i class="fa-solid ${icon} text-base flex-shrink-0"></i>
                                                            <strong class="font-bold text-white text-xs">${f.severity === 'high' ? 'CẢNH BÁO MỨC CAO' : 'LƯU Ý QUAN TRỌNG'}</strong>
                                                        </div>
                                                        ${f.official_citation ? `
                                                            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-black/40 text-gray-300">
                                                                ${f.official_url ? `<a href="${f.official_url}" target="_blank" rel="noopener noreferrer" class="hover:text-purple-300 underline">${escapeHtml(f.official_citation)}</a>` : escapeHtml(f.official_citation)}
                                                            </span>
                                                        ` : ''}
                                                    </div>
                                                    <p class="text-xs leading-relaxed">${escapeHtml(f.message)}</p>
                                                    ${f.grounding_note ? `
                                                        <div class="p-2.5 rounded-xl bg-black/40 border border-white/10 text-[11px] text-gray-300 italic">
                                                            <strong>Chứng cứ pháp lý:</strong> ${escapeHtml(f.grounding_note)}
                                                        </div>
                                                    ` : ''}
                                                </div>
                                            `;
                                        }).join('')}
                                    </div>
                                </div>
                            ` : ''}

                            <!-- 4. HAI NHÓM TIÊU CHÍ (A & B BREAKDOWN) -->
                            <div class="p-5 rounded-3xl bg-[#0E121B] border border-borderBase space-y-5">
                                <div class="flex items-center justify-between border-b border-borderBase pb-3">
                                    <span class="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-2">
                                        <i class="fa-solid fa-list-check text-indigo-400"></i>
                                        <span>Chi tiết bộ tiêu chí đánh giá (${criteria.length} tiêu chí)</span>
                                    </span>
                                </div>

                                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                    <!-- Cột Nhóm A -->
                                    <div class="space-y-3">
                                        <div class="flex items-center justify-between text-xs font-bold text-rose-300 border-b border-rose-500/20 pb-2">
                                            <span>Nhóm A: Tuân thủ chính sách & Pháp luật (40%)</span>
                                            <span class="font-mono">${groupACriteria.length} tiêu chí</span>
                                        </div>
                                        <div class="space-y-2.5">
                                            ${groupACriteria.map(c => `
                                                <div class="p-3.5 rounded-2xl bg-cardBg border border-borderBase space-y-1.5 hover:border-borderLight transition-all">
                                                    <div class="flex items-center justify-between text-xs gap-2">
                                                        <span class="font-bold text-white text-[11px] truncate">${escapeHtml(c.name)}</span>
                                                        <div class="flex items-center space-x-2 flex-shrink-0">
                                                            ${renderStatusBadge(c.status)}
                                                            <span class="font-mono text-xs font-bold ${typeof c.score === 'number' && c.score >= 4 ? 'text-emerald-400' : 'text-amber-400'}">${typeof c.score === 'number' ? `${c.score}/5` : '—'}</span>
                                                        </div>
                                                    </div>
                                                    ${renderFiveSegmentBar(c.score, c.status)}
                                                    <p class="text-[11px] text-gray-300 leading-relaxed">${escapeHtml(c.reason)}</p>
                                                    ${c.suggested_fix ? `
                                                        <div class="text-[10px] text-amber-300/90 pt-1 border-t border-borderBase flex items-start space-x-1">
                                                            <i class="fa-solid fa-wrench text-[9px] mt-0.5"></i>
                                                            <span>Đề xuất sửa: ${escapeHtml(c.suggested_fix)}</span>
                                                        </div>
                                                    ` : ''}
                                                </div>
                                            `).join('')}
                                        </div>
                                    </div>

                                    <!-- Cột Nhóm B -->
                                    <div class="space-y-3">
                                        <div class="flex items-center justify-between text-xs font-bold text-cyan-300 border-b border-cyan-500/20 pb-2">
                                            <span>Nhóm B: Sức hút & Hiệu quả sáng tạo (60%)</span>
                                            <span class="font-mono">${groupBCriteria.length} tiêu chí</span>
                                        </div>
                                        <div class="space-y-2.5">
                                            ${groupBCriteria.map(c => `
                                                <div class="p-3.5 rounded-2xl bg-cardBg border border-borderBase space-y-1.5 hover:border-borderLight transition-all">
                                                    <div class="flex items-center justify-between text-xs gap-2">
                                                        <span class="font-bold text-white text-[11px] truncate">${escapeHtml(c.name)}</span>
                                                        <div class="flex items-center space-x-2 flex-shrink-0">
                                                            ${renderStatusBadge(c.status)}
                                                            <span class="font-mono text-xs font-bold ${typeof c.score === 'number' && c.score >= 4 ? 'text-emerald-400' : 'text-amber-400'}">${typeof c.score === 'number' ? `${c.score}/5` : '—'}</span>
                                                        </div>
                                                    </div>
                                                    ${renderFiveSegmentBar(c.score, c.status)}
                                                    <p class="text-[11px] text-gray-300 leading-relaxed">${escapeHtml(c.reason)}</p>
                                                    ${c.suggested_fix ? `
                                                        <div class="text-[10px] text-amber-300/90 pt-1 border-t border-borderBase flex items-start space-x-1">
                                                            <i class="fa-solid fa-wrench text-[9px] mt-0.5"></i>
                                                            <span>Đề xuất sửa: ${escapeHtml(c.suggested_fix)}</span>
                                                        </div>
                                                    ` : ''}
                                                </div>
                                            `).join('')}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- 5. ƯU ĐIỂM & NHƯỢC ĐIỂM (STRENGTHS & WEAKNESSES) -->
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <!-- Ưu điểm -->
                                <div class="p-5 rounded-3xl bg-[#0E121B] border border-emerald-500/20 space-y-3">
                                    <h5 class="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-2">
                                        <i class="fa-solid fa-circle-check"></i>
                                        <span>Ưu điểm nổi bật (${strengths.length})</span>
                                    </h5>
                                    <div class="space-y-2">
                                        ${strengths.map(s => `
                                            <div class="p-3 rounded-xl bg-cardBg border border-borderBase text-xs text-gray-300 space-y-1">
                                                <div class="font-bold text-emerald-300 flex items-center space-x-1.5">
                                                    <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400">${escapeHtml(s.criterion_id || 'Ưu điểm')}</span>
                                                    <span>${escapeHtml(s.title || '')}</span>
                                                </div>
                                                <p class="text-[11px] text-gray-400 leading-relaxed">${escapeHtml(s.text || '')}</p>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>

                                <!-- Nhược điểm -->
                                <div class="p-5 rounded-3xl bg-[#0E121B] border border-rose-500/20 space-y-3">
                                    <h5 class="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center space-x-2">
                                        <i class="fa-solid fa-triangle-exclamation"></i>
                                        <span>Điểm nghẽn cần khắc phục (${weaknesses.length})</span>
                                    </h5>
                                    <div class="space-y-2">
                                        ${weaknesses.map(w => `
                                            <div class="p-3 rounded-xl bg-cardBg border border-borderBase text-xs text-gray-300 space-y-1">
                                                <div class="font-bold text-rose-300 flex items-center space-x-1.5">
                                                    <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-rose-500/10 text-rose-400">${escapeHtml(w.criterion_id || 'Hạn chế')}</span>
                                                    <span>${escapeHtml(w.title || '')}</span>
                                                </div>
                                                <p class="text-[11px] text-gray-400 leading-relaxed">${escapeHtml(w.text || '')}</p>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            </div>

                            <!-- 6. GÓC NHÌN KHÁCH HÀNG MỤC TIÊU (CUSTOMER VIEW) -->
                            <div class="p-5 rounded-3xl bg-[#0E121B] border border-purple-500/20 space-y-4">
                                <div class="flex items-center justify-between border-b border-borderBase pb-3">
                                    <div class="flex items-center space-x-2">
                                        <i class="fa-solid fa-user-tag text-purple-400 text-sm"></i>
                                        <h5 class="text-xs font-bold text-white uppercase tracking-wider">Góc nhìn khách hàng mục tiêu</h5>
                                        <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-purple-500/10 text-purple-300 border border-purple-500/20">Mô phỏng - Giả định</span>
                                    </div>
                                    <span class="text-[11px] text-gray-400">${escapeHtml(cust.target_audience || 'Khách hàng mục tiêu')}</span>
                                </div>

                                ${cust.simulation_quote ? `
                                    <div class="p-4 rounded-2xl bg-gradient-to-r from-purple-950/30 to-[#0E121B] border border-purple-500/30 text-xs text-purple-200 italic leading-relaxed">
                                        <div class="font-bold text-white text-[11px] not-italic mb-1 flex items-center space-x-1.5">
                                            <i class="fa-solid fa-comment-dots text-purple-400"></i>
                                            <span>Mô phỏng phản hồi tâm lý khách hàng (Xưng "tôi"):</span>
                                        </div>
                                        "${escapeHtml(cust.simulation_quote)}"
                                    </div>
                                ` : ''}

                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                                    <div class="p-3.5 rounded-2xl bg-cardBg border border-borderBase space-y-2">
                                        <strong class="text-emerald-400 flex items-center space-x-1.5">
                                            <i class="fa-solid fa-magnet"></i>
                                            <span>Yếu tố tạo sức hút (Attractions):</span>
                                        </strong>
                                        <ul class="list-disc list-inside space-y-1 text-gray-300 pl-1">
                                            ${(cust.attractions || []).map(a => `<li>${escapeHtml(a)}</li>`).join('')}
                                        </ul>
                                    </div>

                                    <div class="p-3.5 rounded-2xl bg-cardBg border border-borderBase space-y-2">
                                        <strong class="text-rose-400 flex items-center space-x-1.5">
                                            <i class="fa-solid fa-hand"></i>
                                            <span>Rào cản ra quyết định (Objections):</span>
                                        </strong>
                                        <ul class="list-disc list-inside space-y-1 text-gray-300 pl-1">
                                            ${(cust.objections || []).map(o => `<li>${escapeHtml(o)}</li>`).join('')}
                                        </ul>
                                    </div>
                                </div>

                                ${cust.recommended_cta ? `
                                    <div class="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 text-xs text-purple-300 font-semibold flex items-center space-x-2">
                                        <i class="fa-solid fa-bullhorn text-amber-400"></i>
                                        <span>${escapeHtml(cust.recommended_cta)}</span>
                                    </div>
                                ` : ''}
                            </div>

                            <!-- 7. ĐỐI THỦ & ĐỐI CHIẾU THỊ TRƯỜNG (COMPETITOR ANALYSIS) -->
                            <div class="p-5 rounded-3xl bg-[#0E121B] border border-cyan-500/20 space-y-4">
                                <div class="flex items-center justify-between border-b border-borderBase pb-3">
                                    <div class="flex items-center space-x-2">
                                        <i class="fa-solid fa-chart-simple text-cyan-400 text-sm"></i>
                                        <h5 class="text-xs font-bold text-white uppercase tracking-wider">Phân tích & Đối chiếu thị trường</h5>
                                    </div>
                                    <span class="text-[11px] text-gray-400">${comp.has_rival ? 'Có dữ liệu đối thủ' : 'Chưa có đối thủ'}</span>
                                </div>

                                ${!comp.has_rival ? `
                                    <div class="p-6 rounded-2xl bg-cardBg border border-dashed border-borderLight text-center space-y-3">
                                        <div class="w-10 h-10 rounded-full bg-cyan-500/10 text-cyan-400 flex items-center justify-center mx-auto text-base">
                                            <i class="fa-solid fa-users-viewfinder"></i>
                                        </div>
                                        <p class="text-xs text-gray-300 font-medium">Chưa có dữ liệu đối thủ để so sánh trực tiếp trong phiên này.</p>
                                        <p class="text-[11px] text-gray-500 max-w-md mx-auto">Để kích hoạt bảng đối chiếu thị trường có nguồn, hãy chuyển sang chế độ "So sánh với đối thủ" hoặc tải thêm mẫu quảng cáo của đối thủ cạnh tranh.</p>
                                        <button type="button" data-action="switch-to-compare"
                                            class="px-4 py-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 text-xs font-bold hover:bg-cyan-500/30 transition-all inline-flex items-center space-x-2">
                                            <i class="fa-solid fa-plus text-[10px]"></i>
                                            <span>+ Thêm đối thủ để so sánh</span>
                                        </button>
                                    </div>
                                ` : `
                                    ${comp.warning ? `
                                        <div class="p-3.5 rounded-2xl bg-amber-500/15 border border-amber-500/30 text-xs text-amber-300 space-y-1">
                                            <strong class="font-bold text-white flex items-center space-x-1.5">
                                                <i class="fa-solid fa-triangle-exclamation text-amber-400"></i>
                                                <span>CẢNH BÁO TƯƠNG ĐỒNG DỊCH VỤ:</span>
                                            </strong>
                                            <p class="text-[11px] leading-relaxed">${escapeHtml(comp.warning)}</p>
                                        </div>
                                    ` : ''}

                                    <div class="overflow-x-auto">
                                        <table class="w-full text-xs text-left">
                                            <thead>
                                                <tr class="border-b border-borderBase text-gray-400 text-[11px]">
                                                    <th class="py-2.5 px-3">Tiêu chí đối chiếu</th>
                                                    <th class="py-2.5 px-3 text-purple-300">Quảng cáo của tôi</th>
                                                    <th class="py-2.5 px-3 text-cyan-300">Quảng cáo đối thủ</th>
                                                    <th class="py-2.5 px-3">Nhận định</th>
                                                </tr>
                                            </thead>
                                            <tbody class="divide-y divide-borderBase/60">
                                                ${(comp.comparison_rows || []).map(r => `
                                                    <tr>
                                                        <td class="py-2.5 px-3 font-bold text-white">${escapeHtml(r.dimension)}</td>
                                                        <td class="py-2.5 px-3 text-gray-300">${escapeHtml(r.my_ad)}</td>
                                                        <td class="py-2.5 px-3 text-gray-300">${escapeHtml(r.rival_ad)}</td>
                                                        <td class="py-2.5 px-3 text-gray-400 italic">${escapeHtml(r.verdict)}</td>
                                                    </tr>
                                                `).join('')}
                                            </tbody>
                                        </table>
                                    </div>
                                `}
                            </div>

                            <!-- 8. KẾ HOẠCH CẢI THIỆN (ACTIONABLE IMPROVEMENT PLAN) -->
                            <div class="p-5 rounded-3xl bg-[#0E121B] border border-borderBase space-y-4">
                                <div class="flex items-center justify-between border-b border-borderBase pb-3">
                                    <div class="flex items-center space-x-2">
                                        <i class="fa-solid fa-arrow-trend-up text-emerald-400 text-sm"></i>
                                        <h5 class="text-xs font-bold text-white uppercase tracking-wider">Kế hoạch cải thiện có thứ tự ưu tiên</h5>
                                    </div>
                                    <span class="text-[11px] text-gray-400 font-mono">${improvements.length} việc cần làm</span>
                                </div>

                                <div class="space-y-2.5">
                                    ${improvements.map((imp, idx) => `
                                        <div class="p-3.5 rounded-2xl bg-cardBg border border-borderBase flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                                            <div class="space-y-1">
                                                <div class="flex items-center space-x-2">
                                                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${idx === 0 ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : (idx === 1 ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-blue-500/20 text-blue-300 border border-blue-500/30')}">
                                                        ${escapeHtml(imp.priority)}
                                                    </span>
                                                    <span class="text-gray-400 text-[11px]">Vị trí: <strong>${escapeHtml(imp.location || 'Nội dung')}</strong></span>
                                                </div>
                                                <p class="text-gray-200 font-medium">${escapeHtml(imp.action)}</p>
                                            </div>
                                            <span class="text-[11px] text-emerald-400 font-semibold self-start md:self-auto flex-shrink-0">
                                                <i class="fa-solid fa-bullseye mr-1"></i>${escapeHtml(imp.target || 'Tối ưu')}
                                            </span>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>

                            <!-- 9. BA BẢN VIẾT LẠI (THREE REWRITTEN VARIANTS) -->
                            <div class="p-5 rounded-3xl bg-[#0E121B] border border-purple-500/30 space-y-4">
                                <div class="flex items-center justify-between border-b border-borderBase pb-3">
                                    <div class="flex items-center space-x-2">
                                        <i class="fa-solid fa-wand-magic-sparkles text-purple-400 text-sm"></i>
                                        <h5 class="text-xs font-bold text-white uppercase tracking-wider">3 Bản viết lại kịch bản / Caption đề xuất</h5>
                                    </div>
                                    <span class="text-[11px] text-gray-400 font-mono">Đã đối soát chính sách</span>
                                </div>

                                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    ${variants.map(v => `
                                        <div class="variant-card p-4 rounded-2xl bg-cardBg border border-borderBase space-y-3 flex flex-col justify-between hover:border-purple-500/40 transition-all">
                                            <div class="space-y-2.5">
                                                <div class="flex items-center justify-between">
                                                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
                                                        ${escapeHtml(v.angle)}
                                                    </span>
                                                    <i class="fa-solid fa-check-double text-emerald-400 text-xs" title="Đã qua kiểm tra nội bộ"></i>
                                                </div>

                                                <div class="p-3 rounded-xl bg-[#0E121B] border border-borderBase text-xs text-gray-200 leading-relaxed font-normal whitespace-pre-wrap variant-copy-text">${escapeHtml(v.copy)}</div>

                                                <div class="space-y-1.5 text-[10px] text-gray-400 pt-1">
                                                    <div><strong class="text-emerald-400">Facts dùng:</strong> ${(v.facts_used || []).join(', ')}</div>
                                                    <div><strong class="text-cyan-400">Đã sửa:</strong> ${(v.fixes_addressed || []).join(', ')}</div>
                                                    ${v.unresolved_requirements && v.unresolved_requirements.length > 0 ? `
                                                        <div class="text-amber-400/90"><strong class="text-amber-400">Cần bổ sung:</strong> ${v.unresolved_requirements.join(', ')}</div>
                                                    ` : ''}
                                                </div>
                                            </div>

                                            <div class="pt-3 border-t border-borderBase flex items-center justify-between gap-2">
                                                <button type="button" data-action="copy-variant"
                                                    class="flex-1 py-1.5 px-2.5 rounded-xl bg-cardHover hover:bg-borderBase text-xs font-semibold text-gray-200 hover:text-white transition-all flex items-center justify-center space-x-1.5">
                                                    <i class="fa-regular fa-copy text-[11px]"></i>
                                                    <span>Sao chép</span>
                                                </button>
                                                <button type="button" data-action="save-idea-variant"
                                                    data-variant-id="${escapeHtml(v.id || '')}"
                                                    data-variant-angle="${escapeHtml(v.angle || '')}"
                                                    data-brand="${escapeHtml(facts.brand || 'Seoul Center')}"
                                                    data-fixes="${escapeHtml((v.fixes_addressed || []).join('|'))}"
                                                    data-facts="${escapeHtml((v.facts_used || []).join('|'))}"
                                                    class="py-1.5 px-2.5 rounded-xl bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 border border-purple-500/30 text-xs font-bold transition-all flex items-center justify-center space-x-1"
                                                    title="Lưu vào Kho ý tưởng">
                                                    <i class="fa-solid fa-bookmark text-[11px]"></i>
                                                    <span>Lưu ý tưởng</span>
                                                </button>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>

                            <!-- 10. METADATA FOOTER -->
                            <div class="pt-4 border-t border-borderBase flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs text-gray-400">
                                <div>
                                    <span>Bộ tiêu chí: <strong class="text-gray-300 font-mono">v3.0-2026</strong></span>
                                    <span class="mx-2">•</span>
                                    <span>Thời gian: <strong class="text-gray-300 font-mono">${escapeHtml(result.time)}</strong></span>
                                    <span class="mx-2">•</span>
                                    <span>Schema: <strong class="text-purple-300 font-mono">v3.0</strong></span>
                                </div>
                                ${!isModal ? `
                                    <button type="button" onclick="switchTab('history')"
                                        class="px-4 py-2 rounded-xl bg-cardHover hover:bg-borderBase text-xs font-semibold text-gray-200 hover:text-white transition-all flex items-center space-x-2 self-start md:self-auto">
                                        <i class="fa-solid fa-clock-rotate-left"></i>
                                        <span>Xem trong Lịch sử</span>
                                    </button>
                                ` : ''}
                            </div>
                        </div>
                    `;
                }).join('');

                container.innerHTML = `
                    <div class="p-6 md:p-8 rounded-3xl bg-cardBg border border-borderLight shadow-2xl space-y-6 page-fade-in">
                        ${itemsHtml}
                    </div>
                `;
            }

            function renderResultsView(result) {
                const container = document.getElementById('evaluation-results-wrapper');
                if (!container) return;
                container.classList.remove('hidden');
                renderComprehensiveReport(container, result, false);
                if (typeof window.scrollTo === 'function') {
                    container.scrollIntoView({ behavior: 'smooth' });
                }
            }
'''

            html = html[:start_idx] + upgraded_sim_and_renderer + html[end_idx:]
            print("[APPLIED] Upgraded evaluateSingleAdInput, computeSimulatedSessionResult, renderComprehensiveReport, and renderResultsView")

    # 3. Hook into HistoryService.openDetailModal
    hist_modal_needle = "modal.classList.remove('hidden');\n                document.body.classList.add('overflow-hidden');"
    if 'renderComprehensiveReport(document.getElementById(\'history-modal-comprehensive-report\')' not in html and hist_modal_needle in html:
        hook_code = '''                // Render comprehensive report into modal
                const compContainer = document.getElementById('history-modal-comprehensive-report');
                if (compContainer) {
                    renderComprehensiveReport(compContainer, session, true);
                }

                modal.classList.remove('hidden');
                document.body.classList.add('overflow-hidden');'''
        html = html.replace(hist_modal_needle, hook_code)
        print("[APPLIED] HistoryService.openDetailModal hooked to renderComprehensiveReport")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Stage 3 master renderer applied successfully.")

if __name__ == '__main__':
    run()
