import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
import docx
from PIL import Image

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="STRUCT-AI | Kỹ Sư Kết Cấu Đa Phương Thức",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ĐỌC API KEY TỪ .ENV
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY trong file .env! Vui lòng kiểm tra lại.")
    st.stop()

genai.configure(api_key=api_key)
MODEL_NAME = "gemini-3.6-flash"

# HÀM BÓC TÁCH CHỮ TỪ FILE PDF/WORD (NẾU CÓ DÙNG)
def extract_text_from_file(uploaded_file):
    extracted_text = ""
    try:
        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        elif uploaded_file.name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                if para.text:
                    extracted_text += para.text + "\n"
    except Exception as e:
        st.sidebar.error(f"Lỗi khi đọc file: {e}")
    return extracted_text

# 3. GIAO DIỆN CSS CHUYÊN NGÀNH
st.markdown("""
<style>
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    .eng-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
        padding: 22px 26px;
        border-radius: 12px;
        border-left: 6px solid #f59e0b;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .eng-title {
        font-size: 1.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .eng-badge {
        background: #f59e0b;
        color: #0f172a;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
    }
    .tech-tag {
        background: rgba(255,255,255,0.1);
        color: #94a3b8;
        font-size: 0.78rem;
        padding: 3px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .stImage img {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# 4. NÃO BỘ KỸ SƯ TRƯỞNG (HỖ TRỢ THỊ GIÁC HÌNH ẢNH)
SYSTEM_PROMPT = """
Bạn là Kỹ sư Trưởng chuyên ngành Thiết kế Kết cấu Công trình Xây dựng với hơn 15 năm kinh nghiệm.

NĂNG LỰC ĐẶC BIỆT KHI XỬ LÝ HÌNH ẢNH KỸ THUẬT:
1. ĐỐI VỚI BẢN VẼ HOẶC ĐỀ BÀI (Cơ học kết cấu, Sức bền vật liệu):
   - Đọc và nhận diện sơ đồ tính: nhịp dầm, liên kết (ngàm, gối cố định, gối di động), các loại tải trọng (tập trung P, phân bố q, mô-men M).
   - Giải bài toán từng bước rõ ràng: Tính phản lực liên kết -> Lập phương trình nội lực -> Nhận xét biểu đồ.
2. ĐỐI VỚI HÌNH ẢNH MẶT CẮT CẤU KIỆN (Dầm, Cột, Móng, Bố trí thép):
   - Nhận diện kích thước hình học tiết diện, số lượng thanh thép, đường kính thép (D...), lớp bê tông bảo vệ.
   - Đánh giá tính hợp lý theo TCVN 5574:2018 (khoảng hở cốt thép, hàm lượng thép tối thiểu/tối đa).
3. ĐỐI VỚI ẢNH HIỆN TRƯỜNG THI CÔNG (Khuyết tật, nứt, rỗ bê tông):
   - Đưa ra nhận định sơ bộ về dạng nứt (nứt do uốn, nứt do cắt, nứt co ngót) và đề xuất giải pháp xử lý.
4. PHONG CÁCH:
   - Chuyên nghiệp, chuẩn xác về thuật ngữ kỹ thuật kết cấu, xưng hô là 'Tôi' hoặc 'Kỹ sư AI' và gọi người dùng là 'Bạn' hoặc 'Anh/Chị'.
"""

# 5. KHỞI TẠO BỘ NHỚ LỊCH SỬ CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""
if "doc_name" not in st.session_state:
    st.session_state.doc_name = ""

# 6. THANH BÊN (SIDEBAR)
with st.sidebar:
    st.markdown("### 📂 NẠP TÀI LIỆU *(Tùy chọn)*")
    uploaded_file = st.file_uploader("Kéo thả tài liệu PDF/Word:", type=["pdf", "docx"])

    if uploaded_file is not None:
        if st.session_state.doc_name != uploaded_file.name:
            with st.spinner("Đang đọc dữ liệu..."):
                extracted = extract_text_from_file(uploaded_file)
                if extracted:
                    st.session_state.doc_text = extracted
                    st.session_state.doc_name = uploaded_file.name
                    st.success(f"✅ Đã nạp: **{uploaded_file.name}**")
    else:
        st.session_state.doc_text = ""
        st.session_state.doc_name = ""

    if st.session_state.doc_name:
        st.info(f"📄 Đang tra cứu: **{st.session_state.doc_name}**")

    st.divider()
    st.markdown("### 🛠️ TÁC VỤ NHANH")
    selected_prompt = None

    if st.button("📐 AutoLISP vẽ dầm 300x600", use_container_width=True):
        selected_prompt = "Hãy viết mã AutoLISP (.lsp) vẽ mặt cắt dầm 300x600, 3D20 dưới, 2D18 trên, hướng dẫn cách chạy bằng APPLOAD."

    if st.button("📊 Giải Dầm đơn giản L=6m", use_container_width=True):
        selected_prompt = "Giải dầm L=6m chịu tải phân bố q=15 kN/m và P=30 kN tại giữa nhịp. Tính phản lực và viết code Python vẽ biểu đồ M, Q."

    st.divider()
    if st.button("🗑️ Xóa sạch đoạn chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 7. BANNER GIAO DIỆN CHÍNH
st.markdown("""
<div class="eng-banner">
    <div class="eng-title">
        <span>🏗️ STRUCT-AI WORKSPACE</span>
        <span class="eng-badge">VISION & MULTIMODAL</span>
    </div>
    <div style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 10px;">
        Hỗ trợ phân tích ảnh bản vẽ CAD, sơ đồ đề bài Sức bền và tài liệu Kết cấu
    </div>
    <div>
        <span class="tech-tag">📷 Dán ảnh trực tiếp (Ctrl + V)</span>
        <span class="tech-tag">📐 AutoLISP CAD</span>
        <span class="tech-tag">🏢 Revit BIM</span>
        <span class="tech-tag">📊 TCVN 5574 / 2737</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. HIỂN THỊ LỊCH SỬ CHAT (HỖ TRỢ HIỂN THỊ CẢ ẢNH ĐÃ GỬI)
for msg in st.session_state.messages:
    avatar = "👷‍♂️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        if "images" in msg and msg["images"]:
            for img in msg["images"]:
                st.image(img, caption="Ảnh bạn đã gửi", width=420)
        st.markdown(msg["content"])

# 9. Ô NHẬP TIN NHẮN TÍCH HỢP NÚT ĐÍNH KÈM & NHẬN ẢNH DÁN (Ctrl + V)
chat_input_val = st.chat_input(
    "Nhập câu hỏi, hoặc bấm Ctrl+V để dán ảnh bản vẽ / bài tập vào đây...",
    accept_file=True,
    file_type=["png", "jpg", "jpeg", "webp"]
)

# Trích xuất dữ liệu nhập từ người dùng
user_text = ""
user_uploaded_files = []

if selected_prompt:
    user_text = selected_prompt
elif chat_input_val:
    if hasattr(chat_input_val, "text"):
        user_text = chat_input_val.text or ""
    elif isinstance(chat_input_val, dict):
        user_text = chat_input_val.get("text", "")
    else:
        user_text = str(chat_input_val)

    if hasattr(chat_input_val, "files") and chat_input_val.files:
        user_uploaded_files = chat_input_val.files
    elif isinstance(chat_input_val, dict) and chat_input_val.get("files"):
        user_uploaded_files = chat_input_val["files"]

# Khi người dùng gửi câu hỏi hoặc ảnh
if user_text or user_uploaded_files:
    pil_images = []
    if user_uploaded_files:
        for f in user_uploaded_files:
            try:
                pil_images.append(Image.open(f))
            except Exception:
                pass

    # Nếu chỉ dán ảnh mà không gõ chữ, tự tạo câu lệnh phân tích
    if not user_text.strip() and pil_images:
        user_text = "Hãy phân tích hình ảnh kỹ thuật này và giải thích / đưa ra giải pháp kết cấu chi tiết."

    # Lưu và hiển thị tin nhắn của người dùng
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "images": pil_images
    })
    
    with st.chat_message("user", avatar="👤"):
        if pil_images:
            for img in pil_images:
                st.image(img, caption="Ảnh bạn đã tải lên", width=420)
        st.markdown(user_text)

    # Con AI phân tích và trả lời
    with st.chat_message("assistant", avatar="👷‍♂️"):
        message_placeholder = st.empty()

        # Chuẩn bị nội dung gửi lên Gemini
        contents = []
        if st.session_state.doc_text:
            context_text = f"TÀI LIỆU NỘI BỘ THAM KHẢO:\n{st.session_state.doc_text}\n\nYÊU CẦU: {user_text}"
            contents.append(context_text)
        else:
            contents.append(user_text)

        # Đính kèm danh sách ảnh (nếu có)
        for img in pil_images:
            contents.append(img)

        try:
            model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=SYSTEM_PROMPT
            )

            with st.spinner("Kỹ sư AI đang nhìn hình và tính toán nội lực..."):
                response = model.generate_content(contents)
                answer = response.text

            message_placeholder.markdown(answer)
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
        except Exception as e:
            message_placeholder.error(f"Đã xảy ra lỗi: {e}")