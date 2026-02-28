import os
import gradio as gr
from huggingface_hub import InferenceClient

# Lấy token từ Settings → Variables and Secrets
HF_TOKEN = os.getenv("HF_TOKEN")

# Khởi tạo client
client = InferenceClient(token=HF_TOKEN)


def respond(message, history):
    if history is None:
        history = []
        
    # Thêm tin nhắn của người dùng
    history.append({"role": "user", "content": message})
    
    # Chuẩn bị khung cho câu trả lời của Bot
    response_content = ""
    history.append({"role": "assistant", "content": ""})
    
    try:
        # Sử dụng Qwen2.5-72B để đảm bảo độ ổn định và thông minh vượt trội
        stream = client.chat_completion(
            model="Qwen/Qwen2.5-72B-Instruct", 
            messages=history[:-1],  # Gửi lịch sử thực tế (không tính dòng assistant trống)
            max_tokens=1024,
            temperature=0.7,
            stream=True
        )

        for chunk in stream:
            # KIỂM TRA QUAN TRỌNG: Chỉ xử lý nếu chunk có dữ liệu hợp lệ
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                token = chunk.choices[0].delta.content
                if token:
                    response_content += token
                    # Cập nhật nội dung cho tin nhắn cuối cùng
                    history[-1]["content"] = response_content
                    yield "", history

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            history[-1]["content"] = "❌ Lỗi: Bạn chưa cấu hình HF_TOKEN trong Settings của Space."
        else:
            history[-1]["content"] = f"❌ Lỗi kết nối: {error_msg}. Vui lòng thử lại sau vài giây."
        yield "", history


def clear_chat():
    return []


# =========================
# GIAO DIỆN (UI) chuẩn Gradio 5
# =========================
with gr.Blocks(title="Qwen2.5 AI Tutor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Qwen2.5 AI Tutor")
    gr.Markdown("Dự án AI - Trợ lý học tập thông minh.")
    
    # Không để type="messages" vì Gradio 5 đã tự hiểu
    chatbot = gr.Chatbot(height=500, label="Cuộc hội thoại")
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Nhập câu hỏi tại đây...", 
            label="Tin nhắn",
            scale=4
        )
        submit_btn = gr.Button("Gửi", variant="primary", scale=1)

    clear = gr.Button("🗑️ Xóa hội thoại")
    
    # Kết nối sự kiện
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(clear_chat, None, [chatbot])

demo.queue()
demo.launch()