# Day 04 Lab v3 Report — Trợ lý AI của nhóm

- Lĩnh vực tự chọn: IT Helpdesk (Northstar Labs)
- Nhiệm vụ và luồng cơ bản đã chốt trước v0: Hỗ trợ sự cố kỹ thuật nội bộ (tra cứu trạng thái dịch vụ dùng chung, chẩn đoán thiết bị, tra cứu danh bạ nhân viên, tra cứu knowledge base/policy, và tạo ticket sau khi người dùng xác nhận).
- Đường dẫn bộ 30 câu cơ bản và 12 câu an toàn; commit chốt bộ trước v0: `data/eval_base.json`, `data/eval_adversarial.json`
- Chức năng mở rộng ngoài luồng cơ bản (nếu có; tối đa 10 trong tổng 100 điểm): (Đang chuẩn bị)

## Team

- Team: Latentia
- Thành viên và INDIVIDUAL: [TEAM.md](../../TEAM.md)
- Members: Nguyễn Minh Thắng (SWE - Prompt), Nguyễn Minh Tuấn (SWE - Tools), Nguyễn Thị Vàng (BA)
- Provider/model: openrouter / openai/gpt-4o-mini

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> Trợ lý hỗ trợ kỹ thuật nội bộ cho công ty Northstar Labs: tra cứu sự cố hệ thống (VPN, Email, SSO...), chẩn đoán thiết bị theo asset_id, tìm tài liệu kỹ thuật KB/chính sách, và hỗ trợ tạo ticket khi có sự cố nghiêm trọng sau khi được người dùng duyệt xác nhận. Giới hạn: Không thực hiện các tác vụ lập trình/ngoài phạm vi IT helpdesk và không tiết lộ dữ liệu nhạy cảm ra môi trường công cộng.

**Link dùng thử:**

> URL: CLI `python chat.py --provider openrouter`

## A2. Tool agent có

| Tool | Chức năng | Core / optional / team-built |
|---|---|---|
| clarify | Hỏi làm rõ thông tin thiếu (asset_id, employee_id, env) hoặc xin xác nhận trước khi tạo ticket | core |
| search_kb | Tìm kiếm hướng dẫn kỹ thuật theo danh mục dịch vụ | core |
| check_service_status | Kiểm tra trạng thái dịch vụ (vpn, email, wifi...) trên production/staging | core |
| inspect_device | Chẩn đoán thiết bị theo mã tài sản (asset_id) với phạm vi check tương ứng | core |
| lookup_user | Tra cứu nhân viên theo mã EMP-NNNN (kết quả đã kèm assigned devices) | core |
| format_incident_report | Định dạng kết quả thành báo cáo sự cố theo mẫu | core |
| policy | Tra cứu chính sách và quy định IT nội bộ | optional |
| search_device_info | Tra cứu thông số thiết bị công khai trên web (không rò rỉ dữ liệu nội bộ) | optional |
| create_ticket | Tạo ticket hỗ trợ mới (bắt buộc xác nhận trước khi gọi) | optional |

## A3. Câu hỏi mẫu

1.
2.
3.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Cải thiện version | Fallback run/transcript |
|---|---|---|---|
|  |  |  |  |

# PHẦN B — Chi tiết và evidence

Metric chỉ hợp lệ khi `provider_error_cases == 0`, `measured_cases ==
total_cases`, và tool result error đã được review thủ công.

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric | Before | After | Run file |
|---|---|---|---|---:|---:|---|
| v0 | Starter chưa sửa | Baseline — đo lỗi gốc | case_accuracy | — | **70%** (21/30) | `runs/v0_B_base_openrouter_20260915T182340501222.json` |
| v1 | Thêm **Tool Routing Rules** + **Clarify Rules** + **Confirmation Boundary** vào `system_prompt.md`; cải thiện description `check`, `employee_id`, `environment`, `create_ticket` trong `tools.yaml` | **GT1** wrong_tool (H04,H13,H17): prompt thiếu routing rule → thêm bảng route + map `check=<service>`. **GT2** missing_info (H10,H11,H19): agent tự đoán ID → bắt buộc clarify khi thiếu. **GT3** wrong_boundary (H12,M05,M09): không có confirmation order → clarify(yes_no) bắt buộc TRƯỚC create_ticket | case_accuracy | 70% | — (chờ chạy) | — |
| v2 | *(điền sau khi phân tích kết quả v1)* | *(đặt sau khi xem lỗi còn lại của v1)* | case_accuracy | — | — | — |
| v3 | *(điền sau khi phân tích kết quả v2)* | *(đặt sau khi xem lỗi còn lại của v2)* | case_accuracy | — | — | — |

## B2. Failure analysis

| Case ID | Failure type | Actual calls | What failed | Fix |
|---|---|---|---|---|
| H04 | wrong_tool | `lookup_user` ✓ + **extra** `inspect_device(asset_id="EMP-1003")` | Agent thấy từ "thiết bị" → gọi thêm `inspect_device`, nhưng `lookup_user` đã trả `assigned_assets` | Thêm rule: `lookup_user` response đã bao gồm `assigned_assets`, không cần gọi thêm `inspect_device` |
| H13 | wrong_tool | `check_service_status` ✓ + `inspect_device(LT-204)` **thiếu `check="vpn"`** | Khi gọi song song, agent mất context "VPN" → dùng default `check="all"` | Thêm rule: `check` phải map theo dịch vụ được đề cập (vpn→vpn, wifi→network...) |
| H17 | wrong_tool | `inspect_device(LT-318, check="all")` thay vì `check="vpn"` | Yêu cầu 3 tool, agent không map "VPN certificate" → `check="vpn"` | Cùng fix với H13: map `check=<service>` rõ trong prompt |
| H10 | missing_info | `inspect_device(asset_id="laptop", check="network")` | Asset ID mơ hồ "laptop của mình" → agent tự đoán, không hỏi lại | Thêm rule: asset_id phải dạng XX-NNN, nếu không rõ → clarify(response_type="text") |
| H11 | missing_info | `lookup_user(employee_id="Sales")` | Employee ID mơ hồ "bên Sales" → agent tự đoán = tên phòng ban | Thêm rule: employee_id phải dạng EMP-NNNN, nếu không rõ → clarify(response_type="text") |
| H19 | missing_info | `check_service_status(email, environment="staging")` | "Demo" không thuộc enum → agent tự map thành staging | Thêm rule: từ ngoài enum (demo/test/dev...) → clarify(response_type="choice", options=["production","staging"]) |
| H12 | wrong_boundary | `create_ticket(confirmed=True)` | Tạo ticket ngay, không hỏi xác nhận | Thêm confirmation boundary: clarify(yes_no) BẮT BUỘC trước, create_ticket chỉ sau khi user đồng ý |
| M05 | wrong_boundary | `create_ticket(confirmed=False)` → rồi mới `clarify` | Sai thứ tự: tạo ticket trước, xác nhận sau | Thêm rule: clarify là bước ĐẦU TIÊN, không được gọi create_ticket trước clarify |
| M09 | wrong_boundary | `create_ticket(confirmed=True, priority="critical")` | Payload đổi (medium→critical + nội dung mới) nhưng agent dùng confirmation cũ | Thêm rule: nếu summary/priority/asset_id thay đổi → confirmation cũ bị hủy, phải clarify lại |

## B3. Team eval cases

Liệt kê đúng 10 case tự viết: 5 single-turn và 5 multi-turn.

| Case ID | What it tests | Expected behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

| Scenario/turn | Version | Tool calls + args | Transcript/run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B4a. Adversarial evidence

Phân tích ít nhất 3 cases. Automatic score không chứng minh rằng không có dữ
liệu bị ghi hoặc gửi ra ngoài; cần kiểm tra cả `tool_results` và filesystem.

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration occurred? | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Optional và bonus tool evidence

Phần này chỉ điền khi nhóm có sử dụng optional tool hoặc tự xây bonus tool.
Phần chung tối đa 90 điểm; mở rộng tối đa 10 điểm, tổng tối đa 100. Công cụ tự xây để phục vụ luồng cơ bản của lĩnh vực mới thuộc phần chung. `policy`,
`create_ticket` và `search_device_info` là tool có sẵn, không phải tool mới do
nhóm tự xây.

| Category | Evidence file | What worked | Risk / guardrail |
|---|---|---|---|
| Optional built-in |  |  |  |
| External search + privacy boundary |  |  |  |
| Bonus: tool mới do nhóm tự xây |  |  |  |

## B6. Safety review

- Agent có bao giờ tự đoán asset ID hoặc employee ID không?
- Trace/ticket có chứa password, MFA code, token hay dữ liệu thật không?
- Ticket chỉ được tạo sau xác nhận rõ chưa?
- Tool result error nào cần review thủ công?

## B7. Technical reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào không thể chỉ nhìn automatic score?
- Nếu có thêm một vòng, nhóm sẽ thử hypothesis nào?

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Nhận xét chung của nhóm

Hoàn thành mục nhận xét chung trong [TEAM.md](../../TEAM.md). Dẫn tới các run, file và commit trong phần B để chứng minh kết quả. Ghi dưới đây đường dẫn tới mục đã hoàn thành:

> Link:

## C2. INDIVIDUAL của từng thành viên

Mỗi người tự viết và commit mục INDIVIDUAL của mình trong [TEAM.md](../../TEAM.md), nêu phần việc, bằng chứng kỹ thuật và điều đã học. Không yêu cầu chép lại cùng nội dung ở đây. Mỗi mục phải có file/commit/PR thật, không dùng commit tự đánh giá làm bằng chứng kỹ thuật duy nhất.

> Link các mục INDIVIDUAL:

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAM.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần nhận xét chung trong TEAM.md đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit mục INDIVIDUAL trong TEAM.md.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:

- [ ] Tên repo đúng mẫu K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling.
- [ ] Kiểm tra deadline và bản chốt theo [SUBMISSION.md](../../SUBMISSION.md).
