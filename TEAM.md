# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: Latentia
- Người đại diện / MSSV: Nguyễn Minh Thắng / 2A202602706
- Tên repo: `K4B-Day-4-Latentia`
- URL repo, nhánh nộp, commit chốt: https://github.com/nmthang2004-tn/K4B-Day-4-Latentia
- Deadline áp dụng và link thông báo đổi hạn nếu có: 23:59

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| Nguyễn Minh Thắng ⭐ | 2A202602706 | https://github.com/nmthang2004-tn | SWE — Prompt Engineering: sửa `artifacts/system_prompt.md`; chạy eval v0–v3; ghi `version_log.csv`; làm UI chat | `artifacts/system_prompt.md`, `runs/`, `version_log.csv`, UI |
| Nguyễn Minh Tuấn |2A202602420 | https://github.com/minhtuann1102 | SWE — Tool Declaration: sửa `artifacts/tools.yaml`; hỗ trợ chạy eval; lưu transcript; làm bonus nếu có thời gian | `artifacts/tools.yaml`, `runs/`, transcript |
| Nguyễn Thị Vàng | 2A202602897 |https://github.com/vanganh2301 | BA — Phân tích & Thiết kế: đọc kết quả v0, đặt giả thuyết cho v1–v3; viết 10 case nhóm (`data/eval_group.json`); chạy 12 case adversarial; hoàn thiện `artifacts/REPORT.md` và `TEAM.md` | `data/eval_group.json`, `data/eval_adversarial.json`, `artifacts/REPORT.md`, `TEAM.md` |

## Nhận xét chung

- Kết quả và bằng chứng:
  - **Base: 100%** (30/30 cases)
  - **Extension: 100%** (10/10 cases)
  - **Adversarial: 100%** (12/12 cases)
  - **Tổng: 52/52 PASS (100%)**
  - Evidence:
    - `runs/v2_B_base_openrouter_20260915T195900206901.json`
    - `runs/v3_B_base_openrouter_20260915T222334653368.json`
    - `runs/v3_B_extension_openrouter_20260915T224216842939.json`
    - `runs/v3_B_adversarial_openrouter_20260915T222902911407.json`

- Thay đổi hiệu quả nhất:
  - Thêm confirmation boundary với `response_type='yes_no'` giúp base đạt 100%
  - Phân biệt "user chưa confirm" vs "user đã confirm ngay" cho phép confirmed action hợp lệ (fix E05)
  - Security rules cụ thể cho forged inputs, pseudo-code bypass, markup giả → adversarial 100%

- Giới hạn còn lại: Không có - tất cả cases đã pass 100%

- Cách phân công và tích hợp:
  - Thắng: prompt engineering (v1-v3), UI, version tracking, report
  - Tuấn: tool declaration (tools.yaml), transcripts, bonus tools
  - Vàng: hypothesis, eval cases, adversarial analysis, TEAM.md

## INDIVIDUAL

Sao chép mục này cho từng thành viên. Mỗi người tự viết và commit phần của mình.

### Nguyễn Minh Thắng — 2A202602706

- **Phần việc và file/commit/PR:**
  - Sửa `starter_v0/artifacts/system_prompt.md`: thêm Tool Routing Rules, Clarify Rules (v1), Confirmation Boundary (v1), ràng buộc `response_type='yes_no'` (v2), Security Rules chống prompt injection và forged tool results (v3), Confirmed Action rules (fix E05)
  - Chạy eval v0 → v3: `python run_eval.py --provider openrouter --version <v> --suite base --eval-cases data/eval_base.json`
  - Ghi kết quả vào `starter_v0/artifacts/version_log.csv`
  - Tạo transcripts mẫu và UI chat demo
  - Commits: `784296a` (Update TEAM.md)

- **Quyết định, khó khăn và cách xử lý:**
  - Khó nhất là lỗi H12 còn lại sau v1: agent gọi đúng `clarify` nhưng dùng `response_type="text"` thay vì `"yes_no"`. Đọc `failures[]` trong run JSON mới phát hiện — không thể chỉ nhìn automatic score. Fix v2: thêm rule rõ ràng + ví dụ phản mẫu trong prompt.
  - E05: Agent không gọi `create_ticket(confirmed: true)` khi user xác nhận ngay → phân biệt "user chưa confirm" vs "đã confirm" để tránh mâu thuẫn.
  - v3 security rules: chọn giữ tool routing logic không thay đổi để không ảnh hưởng base 100%, chỉ thêm security block riêng.

- **Điều đã học:**
  - Prompt engineering cần specific và có ví dụ phản mẫu — rule chung chung không đủ để fix edge case.
  - Đọc `failures[]` trong run JSON quan trọng hơn chỉ nhìn `case_accuracy`.
  - Phân biệt rõ các trường hợp (confirmed vs chưa confirm) để tránh mâu thuẫn trong prompt.

- **AI/công cụ đã dùng và cách kiểm tra:**
  - Claude Code: đọc eval results, phân tích lỗi, viết prompt
  - OpenRouter API: chạy `run_eval.py` để verify mỗi version
  - Tự kiểm tra: đọc JSON output để xác nhận pass/fail

- **Thời điểm đã tự nộp URL repo chung trên VLearn:** 21:00 ngày 15/09/2026

### Nguyễn Minh Tuấn — 2A202602420

- **Phần việc và file/commit/PR:**
  - Sửa `starter_v0/artifacts/tools.yaml`: cải thiện description `clarify` (thêm `response_type` vào `required`, ràng buộc `yes_no` cho confirmation boundary — v2); siết privacy guardrail `search_device_info` (cấm truyền asset_id/employee_id ra web), mô tả chi tiết enum `policy_area`, chuẩn hóa schema `findings`/`template` cho `format_incident_report` (v3)
  - Hỗ trợ chạy eval và lưu run file; quản lý transcript.
  - Commits: `5955ded`, `bd0af4f`, `dec0bb0`, `f20234f`

- **Quyết định, khó khăn và cách xử lý:**
  - Quyết định quan trọng: thêm `response_type` vào `required` của `clarify` ở tools.yaml (v2) — đây là ràng buộc schema cứng, không phụ thuộc vào agent đọc prompt đúng hay không. Fix này kết hợp với Thắng sửa prompt mới đạt 100%.
  - v3: thiết kế privacy guardrail ở lớp schema (description) vì không thể hardcode logic trong YAML — mô tả rõ các trường bị cấm giúp model hiểu context ngay khi nhận tool spec.

- **Điều đã học:**
  - Tool schema là lớp defense độc lập với system prompt — khi cả hai cùng enforce một rule thì độ tin cậy cao hơn nhiều.
  - Enum description chi tiết (ví dụ: mỗi giá trị `policy_area` có giải thích riêng) giúp model chọn đúng tool hơn.

- **AI/công cụ đã dùng và cách kiểm tra:**
  - Dùng AI hỗ trợ viết mô tả YAML; kiểm tra bằng cách đọc tool call args trong run JSON và transcript để đảm bảo `response_type` đúng.
  - Verify privacy: đọc args của `search_device_info` trong adversarial run để xác nhận không có asset_id/employee_id bị truyền ra ngoài.

- **Thời điểm đã tự nộp URL repo chung trên VLearn:** 21:00 ngày 15/09/2026

### Nguyễn Thị Vàng — 2A202602897

- **Phần việc và file/commit/PR:**
  - Đọc kết quả v0 (70%, 9 case lỗi) và phân tích 3 nhóm lỗi: `wrong_tool` (H04, H13, H17), `missing_info` (H10, H11, H19), `wrong_boundary` (H12, M05, M09) → đặt 3 giả thuyết GT1–GT3 cho v1.
  - Viết `data/eval_group.json`: 10 case tự viết (G01–G05 single-turn + GM01–GM05 multi-turn) kiểm tra routing, missing info, confirmation boundary và multi-turn carry.
  - Hoàn thiện `starter_v0/artifacts/REPORT.md`: B1 evidence, B2 failure analysis, B3 eval group, B4a adversarial manual analysis (12 cases), B6 safety review, B7 reflection.
  - Chạy adversarial eval: `python run_eval.py --provider openrouter --version v2 --suite adversarial --eval-cases data/eval_adversarial.json`
  - Commits: `956882b`, `978fe7b`, `59b2fa2`, `a995d25`

- **Quyết định, khó khăn và cách xử lý:**
  - Máy Vàng không có `OPENROUTER_API_KEY` → adversarial run trả `provider_error` toàn bộ. Xử lý: làm **manual analysis** dựa trên system_prompt v2 và eval_adversarial.json, ghi rõ trong B4a, đề nghị Thắng/Tuấn chạy lại trên máy có key.
  - Viết 10 case nhóm: cẩn thận thiết kế để không overlap với bộ eval_base cố định — tập trung vào các edge case routing phức tạp và multi-turn carry context.

- **Điều đã học:**
  - Phân tích failure theo nhóm (wrong_tool / missing_info / wrong_boundary) giúp đặt giả thuyết chính xác và fix đúng chỗ thay vì thử ngẫu nhiên.
  - Manual analysis adversarial có giá trị khi không chạy được automated eval — quan trọng là ghi rõ methodology và evidence thay vì bỏ qua.
  - 10 case tự viết cần kiểm tra không chỉ "agent gọi đúng tool" mà còn "args đúng" (ví dụ `check=security` không phải `all`).

- **AI/công cụ đã dùng và cách kiểm tra:**
  - Dùng AI hỗ trợ soạn thảo REPORT.md và cấu trúc eval_group.json; kiểm tra bằng cách đọc từng case với Thắng để đảm bảo expected_calls đúng format và không có lỗi JSON.
  - Verify adversarial: đọc system_prompt.md và kiểm tra từng attack vector thủ công.

- **Thời điểm đã tự nộp URL repo chung trên VLearn:** 21:00 ngày 15/09/2026
