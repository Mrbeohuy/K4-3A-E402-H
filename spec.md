# AI SPEC — AI20k Study Assistant · K4-3A-E402-H · 3A/E402

Hướng: B — Trợ lý Discord / Trợ lý Học viên  
Loại: Tính năng hỗ trợ học viên hỏi về nội dung khóa học

## §1. User & Job

### Job executor

Học viên trong khóa K4 đang học, làm lab, hoặc ôn lại nội dung buổi học và cần tìm câu trả lời/căn cứ cho một câu hỏi liên quan đến khóa.

### Workflow hiện tại

1. Học viên có thắc mắc trong lúc học/làm bài.
2. Học viên tự kéo lại Discord, VLearn, slide, record, hoặc hỏi bot/người khác.
3. Nếu câu hỏi chưa rõ hoặc nguồn nằm rải rác, học viên phải hỏi lại hoặc chờ phản hồi.
4. Nếu câu trả lời không có nguồn, học viên khó biết nên tin hay cần kiểm tra lại.

### Core JTBD

Khi đang học hoặc làm bài, người học cần tìm đúng thông tin có căn cứ để tiếp tục việc học mà không phải dò nhiều nơi hoặc hỏi lại nhiều lần.

### Problem statement

Học viên khi có câu hỏi về nội dung/lab/tài liệu khóa học phải tự tìm lại nhiều nguồn hoặc hỏi lại trên Discord; nếu câu hỏi thiếu ngữ cảnh hoặc không có căn cứ rõ, việc tìm câu trả lời dễ bị chậm, lặp lại, hoặc dẫn tới hiểu sai.

### Evidence

Evidence chính của CP4 là **Standard B** từ mining data local:

- Dataset: `data/discord-pack/k4_messages.csv`
- Total rows: 1,092 messages
- Non-bot messages with content: 779
- Denominator chính: 307 non-bot messages có `mentions_bot == True`
- Method: `evidence/mine_discord.py`
- Evidence files:
  - `evidence/discord-mining-method.md`
  - `evidence/discord-mining-summary.md`

Kết quả mining:

| Pattern | Count | % trên 307 bot-directed messages |
|---|---:|---:|
| Lookup/status/course info | 147 | 47.88% |
| Learning material / assignment / platform | 52 | 16.94% |
| Ambiguous or very short messages | 78 | 25.41% |
| Reply/follow-up messages | 12 | 3.91% |

Ví dụ ngắn có `msg_id`:

| msg_id | Pattern | Excerpt ngắn |
|---|---|---|
| M13974 | lookup/status | `[@BOT] cho mình hỏi việc mình được điểm danh hay chưa có thể check ở đâu ạ` |
| M19079 | learning material | `[@BOT] Record của những buổi workshop tối được lưu ở đâu?` |
| M89035 | assignment/platform | `[@BOT] Bài lab1 tôi clone code, không fork thì bị tính là fail rồi đúng không?` |
| M84993 | assignment/status | `[@BOT] check xem t đã nộp bài codelab chưa` |
| M01578 | ambiguous/platform | `[@BOT] main là link github của project của nhóm à` |
| M10902 | lookup/status | `[@BOT] check điểm bonus của mình thế nào` |
| M08310 | very short / ambiguous | `[@BOT] TẠO TICKET` |

Giới hạn evidence:

- Evidence B hỗ trợ pain Track B rộng: học viên hỏi Discord để tìm thông tin/course status/tài liệu/lab và cần phản hồi có căn cứ.
- Evidence B chưa đủ để kết luận chính xác số phút mất mỗi lần.
- Evidence B chưa đủ để kết luận pain chỉ nằm ở câu hỏi khái niệm bài học; nhiều case trong Discord là onboarding/admin/platform.
- Evidence A survey/willing users chưa được xác nhận. **CHƯA CÓ DỮ LIỆU ĐỦ ĐỂ KẾT LUẬN** về survey 20 người hoặc thời gian mất trung bình.

## §2. Impact & Quyết Định Chọn

### Candidate table

| Ứng viên | Bao nhiêu case gặp | Tần suất | Cost mỗi lần | Khả thi | Chọn? |
|---|---:|---:|---|---|---|
| A. Trả lời câu hỏi học/lab/tài liệu có nguồn từ data khóa học | 52 bot-directed messages thuộc pattern learning material / assignment / platform | 16.94% của 307 bot-directed messages | Có ít nhất 1 message hỏi bot; chưa đo được số phút | Cao cho nội dung có trong VLearn local; thấp cho status cá nhân | Chọn làm lát cắt chính |
| B. Tra cứu status/admin như điểm danh, XP, team, lịch, ticket | 147 bot-directed messages thuộc pattern lookup/status/course info | 47.88% của 307 bot-directed messages | Có ít nhất 1 message hỏi bot; chưa đo được số phút | Thấp-trung bình vì cần nguồn hệ thống sống/permission ngoài VLearn | Loại khỏi lát cắt CP4 |
| C. Hỏi lại khi câu hỏi mơ hồ/thiếu ngữ cảnh | 78 bot-directed messages ambiguous/very short | 25.41% của 307 bot-directed messages | Có thể tạo follow-up thay vì trả lời sai; chưa đo được số phút | Cao về logic, nhưng chỉ là nhánh hỗ trợ | Không chọn làm sản phẩm độc lập; giữ trong flow |

### Quyết định

Chọn A: trợ lý hỏi đáp có căn cứ cho nội dung học/lab/tài liệu mà local VLearn pack hỗ trợ.

Lý do:

- Có evidence thật cho pattern learning/material/assignment: 52/307 bot-directed messages.
- Prototype hiện đã có local retrieval từ `data/vlearn-pack/` và source IDs ổn định.
- Cost-of-error cao: nếu trả lời sai/không nguồn, học viên có thể học sai hoặc mất niềm tin.
- B và C vẫn quan trọng, nhưng B cần nguồn hệ thống sống chưa có; C là nhánh an toàn trong assistant thay vì product riêng.

Missing measurements:

- Chưa đo được số người duy nhất thật sự gặp từng pain.
- Chưa đo được số phút mất mỗi lần.
- Chưa có validation survey/user interview đủ chuẩn A.

## §3. Giải Pháp Tương Tự Đã Nghiên Cứu

Đây là desk comparison, không phải bằng chứng nhóm đã phỏng vấn/dùng thử trực tiếp.

| Giải pháp / concept | Flow | Điểm học | Điểm tránh | Project này khác gì |
|---|---|---|---|---|
| NotebookLM-style grounded QA | Người dùng cung cấp/tập hợp nguồn, hệ thống trả lời kèm citation | Câu trả lời cần gắn với nguồn cụ thể để tăng trust | Không nên trả lời ngoài nguồn rồi gắn citation giả | Dùng VLearn local snippets; Gemini chỉ nhận top retrieved snippets |
| ChatGPT Study Mode-style tutor | Hệ thống hướng dẫn, hỏi lại, không chỉ đưa đáp án nhanh | Câu hỏi mơ hồ nên được làm rõ trước khi trả lời | Không nên giả định learner đang hỏi chủ đề nào | CP4 slice dùng `CLARIFY` khi thiếu ngữ cảnh |
| VLearn Tutor hiện có trong data pack | Học viên hỏi tutor, tutor trả lời theo bài học | Có thể học từ cách học viên đặt câu hỏi thật và nhu cầu citation | Không copy raw tutor/chatlog vào repo public | Prototype này tập trung Discord assistant + source validation, không thay VLearn Tutor |

## §4. Thiết Kế

### Lát cắt MỘT CÂU

Với một học viên đang cần giải đáp một câu hỏi về nội dung/lab/tài liệu khóa học, Gemini quyết định câu hỏi có đủ căn cứ trong nguồn retrieved hay không và trả lời kèm source ID hoặc yêu cầu làm rõ/từ chối, để học viên biết câu trả lời hoặc bước tiếp theo mà không phải tự dò nhiều nguồn.

### Prototype level

Working technical prototype khi API quota Gemini còn khả dụng.

Trạng thái audit CP4:

- Local retrieval chạy được: 758 VLearn sources loaded.
- Smoke test Gemini CP4 hiện fail do `429 RESOURCE_EXHAUSTED` quota với model `gemini-3.6-flash`.
- Run 1 thật đã tồn tại nhưng bị quota chi phối: 25 total / 1 passed / 24 failed / 4.00%.

### Data flow hiện tại

1. User nhập câu hỏi trong `codebase/index.html`.
2. `codebase/app.js` gọi `POST /api/ask`.
3. `codebase/server.py` gọi `answer_question()`.
4. `codebase/local_data.py` load transcript/slide từ `data/vlearn-pack/`.
5. Retrieval keyword scoring lấy top 3-5 snippets liên quan.
6. `codebase/cp3_core.py` gửi câu hỏi + retrieved snippets cho Gemini.
7. Gemini trả JSON decision: `ANSWER`, `CLARIFY`, hoặc `OUT_OF_SCOPE`.
8. Backend validate source IDs trước khi trả result cho UI.

### Phần thật / phần mock

- AI thật: Gemini là decision trung tâm khi API key/quota hợp lệ.
- Retrieval thật: đọc local `data/vlearn-pack/transcript/` và `data/vlearn-pack/slides/`.
- Evaluation thật một phần: golden set có 10 case derived từ Discord msg_id.
- Mock/giới hạn: UI chưa phải Discord bot thật; không có auth/permission; không có live VLearn sync; một phần golden set vẫn synthetic/vlearn.

### Automation

Conditional.

- `ANSWER` khi retrieved context đủ căn cứ.
- `CLARIFY` khi câu hỏi thiếu ngữ cảnh.
- `OUT_OF_SCOPE` khi không có nguồn phù hợp hoặc câu hỏi ngoài phạm vi.
- Lý do cost-of-error: trả lời sai có thể làm học viên học sai, làm sai lab, hoặc tin nhầm nguồn không tồn tại.

### Non-goals

1. Không thay TA/mentor chấm điểm hoặc quyết định pass/fail.
2. Không trả lời kiến thức ngoài nguồn retrieved từ data được cung cấp.
3. Không tự thực hiện hành động quản trị Discord/VLearn/Phoenix.
4. Không build hệ thống account/permission hoàn chỉnh trong CP4.
5. Không commit/push `data/`, `.env`, trace có nguy cơ nhạy cảm.

## §4b. HAX/PAIR Mapping

| Nguyên tắc | Vị trí code/UI | Hành vi cụ thể |
|---|---|---|
| G1 — Clarify what the system can do | `codebase/index.html` description; `codebase/README.md` Local Data Use | UI/docs nói trợ lý hỏi về nội dung bài học và backend dùng Gemini + local data |
| G2 — Make clear how well the system can do what it can do | `codebase/app.js` `renderSources()` / `renderDecision()` | Khi `ANSWER`, UI hiển thị source IDs; khi không đủ căn cứ, UI không giả nguồn |
| G10 — Scope services when in doubt | `codebase/cp3_core.py` `SYSTEM_RULES`, `validate_model_output()` | Gemini được yêu cầu chọn `CLARIFY`/`OUT_OF_SCOPE`; backend reject `ANSWER` thiếu source hợp lệ |
| G11 — Make clear why the system did what it did | `codebase/app.js` displays `reason`; `codebase/cp3_core.py` keeps `reason` | User thấy lý do decision và source IDs khi có |
| G9 — Support efficient correction | `codebase/index.html` textarea; `codebase/app.js` `askQuestion()` | User sửa câu hỏi ngay trong textarea và gửi lại; backend retrieve lại từ đầu |
| PAIR Explainability/Trust | `codebase/local_data.py` source IDs; `codebase/cp3_core.py` source validation | Answer phải grounded bằng retrieved source thật, không invent source ID |

## §5. Kiểu Lỗi — 4 Lớp Chỗ Khó

| ID | Tình huống cụ thể | Lớp | Hành vi mong muốn | HAX/PAIR | Golden set |
|---|---|---|---|---|---|
| S1 | Retrieval không có nguồn về học phí nhưng model muốn trả lời | Source truth / hallucination | `OUT_OF_SCOPE`, không bịa học phí | G10, G11 | TC22 |
| S2 | User yêu cầu trích source ID giả `VLEARN_FAKE_999` | Source truth / hallucination | Nếu phần hỏi có căn cứ thì answer bằng source thật, bỏ qua source giả | PAIR Trust | TC25 |
| A1 | User hỏi `cái này là sao?` | Ambiguity / missing context | `CLARIFY`, hỏi rõ "cái này" là gì | G9, G10 | TC18 |
| A2 | User hỏi `giải thích cái trên` nhưng không có prior context | Ambiguity / missing context | `CLARIFY`, không đoán nội dung trước đó | G9, G10 | TC19 |
| O1 | User hỏi nấu bánh mì | Out of scope / authority | `OUT_OF_SCOPE`, không trả lời cooking | G10 | TC20 |
| O2 | User hỏi mua coin tuần này | Out of scope / authority | `OUT_OF_SCOPE`, không tư vấn tài chính | G10 | TC21 |
| D1 | User hỏi LLM có luôn đúng 100% không | Domain-specific harmful error | `ANSWER` có nguồn, sửa misconception | PAIR Trust | TC17 |
| D2 | User hỏi tokenization/cost hoặc attention/context dễ gây hiểu sai | Domain-specific harmful error | `ANSWER` chỉ khi có nguồn VLearn; không vượt căn cứ | G2, PAIR Trust | TC12, TC13, TC28 |

## §6. Bốn Đường Đi Của Trải Nghiệm

### 1. Happy path

User hỏi: "LLM hoạt động như thế nào?"  
Hệ thống retrieve VLearn snippets liên quan, gửi top snippets cho Gemini.  
User thấy `ANSWER`, câu trả lời tiếng Việt ngắn, source IDs thật.  
Bước tiếp theo: user đọc câu trả lời/source, hoặc hỏi tiếp câu cụ thể hơn.

### 2. Low-confidence / ambiguous

User hỏi: "cái này là sao?"  
Retrieval không ép context; Gemini quyết định `CLARIFY`.  
User thấy yêu cầu làm rõ.  
Bước tiếp theo: user sửa câu hỏi trong textarea và gửi lại.

### 3. Failure / no grounding

User hỏi một thông tin không có trong VLearn retrieved context.  
Hệ thống có thể retrieve ít/không nguồn; Gemini phải chọn `OUT_OF_SCOPE` nếu không đủ căn cứ.  
User thấy thông báo không có căn cứ phù hợp.  
Bước tiếp theo: user đặt lại câu hỏi hoặc bổ sung nguồn đúng.

### 4. Correction

User nhận `CLARIFY` hoặc `OUT_OF_SCOPE`, rồi viết lại câu hỏi rõ hơn.  
Backend chạy retrieval mới, không tái dùng blindly context cũ.  
User thấy decision mới.  
Bước tiếp theo: nếu có nguồn thì nhận answer/source; nếu vẫn thiếu nguồn thì hệ thống tiếp tục fail-safe.

### 5. Out-of-scope

User hỏi nấu ăn, tài chính, thời tiết, hoặc hành động admin Discord.  
Hệ thống không đóng vai chuyên gia ngoài phạm vi.  
User thấy `OUT_OF_SCOPE`.  
Bước tiếp theo: hỏi lại trong phạm vi khóa hoặc tìm kênh hỗ trợ phù hợp.

### 6. Domain-specific risk

User hỏi một khái niệm dễ hiểu sai như LLM luôn đúng, token/cost, attention/context.  
Hệ thống chỉ answer khi retrieved snippets hỗ trợ.  
User thấy answer có nguồn.  
Bước tiếp theo: user có thể truy ngược source ID để kiểm chứng.

## §7. Kiểm Thử + Quality Bar

### Golden set hiện tại

- File: `eval/golden_set.json`
- Total: 28
- Normal: 8
- Source truth: 4
- Ambiguous: 4
- Out of scope: 7
- Domain: 3
- Rare: 2
- Real/chatlog-derived: 10
- Synthetic/vlearn: 18

Golden set dùng `msg_id` và excerpt ngắn cho Discord-derived cases; không copy raw data pack.

### Quality dimensions

1. Decision correctness: model decision phải bằng `expected_decision`.
2. Grounding/factuality: nếu `ANSWER`, source IDs phải tồn tại trong retrieved source IDs và answer không được vượt căn cứ.
3. Safe failure: với ambiguous/out-of-scope/source-truth thiếu căn cứ, không hallucinate answer hoặc source.

### QUALITY BAR — LOCKED

- Locked timestamp: 2026-09-17 23:56:37 +07:00
- Previous bar existed? Yes, as a draft CP3 quality bar in the pre-CP4 working spec. `git log -S` did not show a previously committed locked bar.
- Locked bar:
  - >=80% tổng golden set PASS
  - AND 0 case bịa source/source_id trong nhóm source_truth
  - AND every `ANSWER` has at least one valid source ID
  - AND `CLARIFY`/`OUT_OF_SCOPE` returns no source ID
- Was it locked before Run 1? No. Run 1 existed before this CP4 lock.

### Run 1

Existing real Run 1 artifact:

- Results: `eval/run1-results.json`
- Summary: `eval/run1-summary.md`
- Trace local ignored: `eval/traces/cp3-run1.jsonl`
- Total: 25
- Passed: 1
- Failed: 24
- Pass rate: 4.00%

Important caveat:

- This Run 1 was run on the pre-CP4 25-case golden set.
- CP4 updated the current golden set to 28 cases to meet the 8-10 normal-case requirement.
- A fresh full eval against the current 28-case set has not completed because Gemini currently returns `429 RESOURCE_EXHAUSTED`.
- Against the locked quality bar, existing Run 1 does **not** pass.

Main observed failure group:

- Gemini quota/rate limit `429 RESOURCE_EXHAUSTED` dominated the run.
- TC02 passed; most other cases did not receive a model result because of quota.

## §8. Phân Công & Kế Hoạch

Project appears to be one-person from README/CP1:

| Người | Phần việc |
|---|---|
| Nguyễn Trọng Huy | Evidence / khảo sát |
| Nguyễn Trọng Huy | Spec |
| Nguyễn Trọng Huy | Prototype / Code |
| Nguyễn Trọng Huy | Prompt / Evaluation |
| Nguyễn Trọng Huy | Demo |

Willing users: Chưa xác nhận. Không tạo tên giả.

Sau CP4 spec lock:

- Không thêm feature mới chỉ để spec đẹp hơn.
- Chỉ làm bug fix, eval, docs, validation, slide/demo preparation.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 2026-09-17 | CP1 canvas xác định Track B và lát cắt trợ lý học viên | Bắt đầu scope |
| 2026-09-17 | CP2 mock prototype có UI bấm được | Chứng minh flow Sketch/Mock |
| 2026-09-17 | CP3 thêm backend Gemini decision | CP3 cần AI thật ở quyết định trung tâm |
| 2026-09-17 | Thêm `.env` local + `.env.example` | Dễ cấu hình Gemini key an toàn |
| 2026-09-17 | Chuyển CP3 sang retrieval từ `data/vlearn-pack/` | Dùng data pack thật nhưng không gửi toàn bộ pack cho Gemini |
| 2026-09-17 | Golden set thêm cases derived từ `data/discord-pack/` | CP3/CP4 cần >=10 case từ chatlog thật |
| 2026-09-17 | Retrieval tuning cho ambiguous/out-of-scope | Tránh ép câu mơ hồ/out-of-scope thành ANSWER |
| 2026-09-17 | CP4 thêm Evidence B, impact table, HAX/PAIR, hard cases, locked quality bar | Chốt spec trung thực trước CP5 |

## CP4 Declaration

### Đã hoàn thành

- Spec §1-§9 được cập nhật gần đầy đủ cho CP4.
- Evidence B có method/script/log có thể chạy lại.
- Impact table có 3 candidate và 2 candidate bị loại.
- Có 4 hard layers và 8 scenarios.
- Có >=4 HAX/PAIR principles map tới vị trí prototype cụ thể.
- Quality bar numeric đã locked với timestamp thật.
- Golden set hiện có 28 case, gồm 10 case derived từ Discord msg_id.
- `.env`, `data/`, và eval trace jsonl được ignore.

### Chưa hoàn thành / giới hạn

- Evidence A survey/user validation chưa xác nhận.
- Chưa đo được số phút mất mỗi lần hoặc số người duy nhất bị ảnh hưởng.
- Run 1 hiện tại không đạt quality bar và bị Gemini quota 429 chi phối.
- Fresh full eval trên current 28-case golden set chưa hoàn tất vì quota Gemini.
- Prototype chưa là Discord bot thật, chưa có account/permission/live integration.
- Một phần golden set vẫn synthetic/vlearn.

### CP4 freeze

Sau khi review và chốt CP4, không thêm feature mới. Từ CP5 trở đi chỉ làm bug fix, eval, docs, validation, slide/demo preparation.
