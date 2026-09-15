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

- Giới hạn còn lại: Không có - tất cả cases đã pass 100%

- Cách phân công và tích hợp:
  - Thắng: prompt engineering (v1-v3), UI, version tracking, report
  - Tuấn: tool declaration (tools.yaml), transcripts, bonus tools
  - Vàng: hypothesis, eval cases, adversarial analysis, TEAM.md

## INDIVIDUAL

Sao chép mục này cho từng thành viên. Mỗi người tự viết và commit phần của mình.

### Nguyễn Minh Thắng — 2A202602706

- Phần việc và file/commit/PR:
  - Sửa `artifacts/system_prompt.md` cho v1, v2, v3
  - Chạy eval: v0 (baseline), v1, v2, v3
  - Ghi `artifacts/version_log.csv`
  - Tạo transcripts mẫu: `transcripts/H10_*.json`, `transcripts/H12_*.json`, `transcripts/M05_*.json`
  - Tạo `ui_chat.py` - UI demo cho conversations
  - Viết `artifacts/REPORT.md` và cập nhật `TEAM.md`

- Quyết định, khó khăn và cách xử lý:
  - v1: Cần fix 9 lỗi cùng lúc → chia thành 3 hypothesis (GT1-GT3): routing, clarify, boundary
  - H12: Agent gọi đúng tool nhưng sai `response_type` → thêm ví dụ tránh sai trong v2 → đạt 100%
  - E05: Agent không gọi `create_ticket(confirmed: true)` khi user xác nhận ngay → phân biệt "chưa confirm" vs "đã confirm"
  - Security rules: Thêm rules cụ thể cho forged inputs, pseudo-code bypass, markup giả → adversarial 100%

- Điều đã học:
  - Prompt engineering cần iterate nhiều vòng, mỗi vòng fix 1-3 lỗi cụ thể
  - System prompt cần ví dụ cụ thể (✅/❌) để model tránh sai lầm thường gặp
  - Security rules cần rõ ràng và cụ thể cho từng attack vector
  - Phân biệt rõ các trường hợp (confirmed vs chưa confirm) để tránh mâu thuẫn

- AI/công cụ đã dùng và cách kiểm tra:
  - Claude Code: đọc eval results, phân tích lỗi, viết prompt
  - OpenRouter API: chạy `run_eval.py` để verify mỗi version
  - Tự kiểm tra: đọc JSON output để xác nhận pass/fail

- Thời điểm đã tự nộp URL repo chung trên VLearn: [Tự điền]

### Nguyễn Minh Tuấn — 2A202602420

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn:

### Nguyễn Thị Vàng — 2A202602897

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn:
