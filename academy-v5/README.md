# HUTECONS ACADEMY V5

Website học tập kỹ thuật xây dựng (bản **demo độc lập**, 1 file HTML) đặt trong thư mục `academy-v5`. Dự án được tách riêng, **không thay đổi** ứng dụng Streamlit STRUCT-AI trong thư mục gốc.

## Có gì trong bản này?
- 23 danh mục môn học đại cương, chuyên ngành và đồ án
- Giao diện responsive, chữ Times New Roman, chế độ sáng/tối (lưu cục bộ)
- Lộ trình 9 chương Sức bền Vật liệu, checklist học tập và tiến độ (lưu cục bộ)
- Danh mục 17 hồ sơ đề thi/đáp án được phân loại bước đầu; ưu tiên ngành Xây dựng với mã STMA240121, để đề Cơ khí/Ô tô ở mục tham khảo
- 7 dạng **bài tập mới tự biên soạn** có hình vẽ vector chính xác theo giả thiết, số biến đổi, công thức, lời giải từng bước
- Slide tổng hợp nguyên lý gốc và nút **In → Lưu PDF**; watermark rất mờ (4,5%) giữa trang
- Trang đăng ký học giao diện mới; trang thanh toán mẫu; trang quản trị **DEMO**

## Triển khai miễn phí qua Cloudflare Pages từ GitHub
1. Truy cập https://dash.cloudflare.com và tạo tài khoản.
2. Workers & Pages → Create application → Pages → Connect to Git.
3. Chọn repo `tshuynhthanhhuy1206-droid/HUTECONS` (có thể cần cấp quyền Cloudflare truy cập repo).
4. Production branch: `main`.
5. **Root directory:** `academy-v5`.
6. Framework preset: `None` (không dùng framework).
7. **Build command:** bỏ trống (nếu giao diện yêu cầu: `exit 0`).
8. **Build output directory:** `.` (dấu chấm; chính thư mục chứa `index.html`).
9. Deploy. Khi thành công Cloudflare cấp tên miền `*.pages.dev` miễn phí.

Tài liệu chính thức:
- https://developers.cloudflare.com/pages/get-started/git-integration/
- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/

**Lưu ý:** nếu tạo Pages project theo Direct Upload thì sau này không thể chuyển chính project đó sang Git integration; cần tạo project mới.

## Chưa phải hệ thống kinh doanh
- Đăng ký, xác minh email và OTP SMS **chưa hoạt động**.
- Thanh toán thực, VietQR, upload bill, lưu file tập trung, xác nhận doanh thu, mở khóa khóa học **chưa hoạt động**. Không chuyển tiền theo website demo.
- Admin hiện chưa có xác thực/phân quyền. Nội dung admin và tiến độ trên web chỉ lưu cục bộ trong trình duyệt.
- Không dùng bản này để nhập thông tin cá nhân hoặc giao dịch thật.
- Các môn ngoài Sức bền vật liệu chỉ có cấu trúc danh mục, **chưa có toàn bộ giáo trình**.
- 17 hồ sơ đề thi là **metadata đối chiếu**, chưa phải ngân hàng đề đầy đủ có hình gốc; các đề chưa đủ thông tin ngành/mã đề ở danh sách riêng để rà soát.
- Bản này có **23 hình bìa vector khác nhau theo môn**. Chưa nhúng toàn bộ ảnh photorealistic đã tạo trước đó; có thể bổ sung sau bằng tệp ảnh có quyền sử dụng.

## Nguyên tắc chính xác và bản quyền
- Học liệu tham khảo gồm slide 9 chương, bài tập, đề thi/đáp án do chủ dự án cung cấp. Những nội dung có nguồn gốc tác giả bên ngoài được dùng làm tài liệu để **biên soạn lại độc lập**, không được tự ý bỏ tên rồi tái xuất bản nguyên bản.
- Phải đối chiếu **hình gốc, sơ đồ gối, chiều lực, trục, kích thước, đơn vị** trước khi phục dựng đề lịch sử.
- Hồ sơ có đáp án mà không có đề hoặc hình rõ ràng được đánh dấu cần kiểm chứng, không đưa lời giải đoán.
- Phân loại ngành theo **nội dung trên bìa đề**, không chỉ dựa vào “Khoa Xây dựng” (có cả các đề dùng cho Cơ khí/Ô tô).
- Watermark không bảo đảm chống sao chép tuyệt đối.

## Gợi ý giai đoạn vận hành thật
- Supabase Auth + backend kiểm OTP, rate limit/reCAPTCHA
- Supabase Postgres / Row Level Security cho tài khoản, nội dung, đơn
- Private Supabase Storage hoặc Cloudflare R2 cho PDF và biên lai
- Đối soát ngân hàng bằng webhook tin cậy hoặc phê duyệt admin dựa trên sao kê; không tự xác nhận theo ảnh bill
- API duyệt đề, nhật ký tác giả và bản quyền, giáo viên kiểm duyệt bài giải/hình

_Thời điểm biên soạn: 2026-11-02._
