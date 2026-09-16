# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 17/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — [Tên lát cắt] · Nhóm [XX] · Zone [X]
Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [ ] Tính năng mới

## §1. User & Job

- Job executor:
  Học viên AI20k đang học hoặc ôn lại bài và cần tìm câu trả lời
  cho một câu hỏi liên quan đến nội dung khóa học.

- Problem statement:
  Học viên khi có câu hỏi về nội dung bài học phải tự tìm lại
  slide, video, tin nhắn Discord hoặc chờ người khác trả lời;
  nếu không biết thông tin nằm ở đâu, việc tìm câu trả lời có thể
  mất thời gian và làm gián đoạn quá trình học.

- Evidence:
  - CP1: đang thu khảo sát.
  - Evidence 1: [quote thật]
  - Evidence 2: [quote thật]

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):
- Ứng viên ĐÃ LOẠI + vì sao:
- Ứng viên CHỌN + vì sao (bằng số):

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế

- Lát cắt MỘT CÂU:
  Với một học viên AI20k đang cần giải đáp một câu hỏi về nội dung
  khóa học, AI quyết định câu hỏi có đủ căn cứ để trả lời hay không
  và trả lời kèm nguồn hoặc yêu cầu làm rõ, để học viên biết được
  câu trả lời hoặc bước tiếp theo mà không phải tự dò nhiều nguồn.

- Mức prototype nhắm tới:
  Mock.

- Automation:
  Conditional — chỉ tự trả lời khi có căn cứ phù hợp; câu hỏi mơ hồ
  hoặc không có căn cứ thì yêu cầu làm rõ.

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
```
