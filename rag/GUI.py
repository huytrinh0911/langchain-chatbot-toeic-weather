# app.py
import gradio as gr
import agent

# --------- Hàm xử lý chat ----------
def respond(user_message, chat_history):
    if not user_message or not user_message:
        return chat_history, gr.update(value="")
    user_bubble = f"{user_message}🧑"
    bot_reply = f"🤖 {agent.chat_with_agent(user_message)}"
    chat_history = chat_history + [(user_bubble, bot_reply)]
    return chat_history, gr.update(value="")

def clear_chat():
    agent.memory.clear()
    return [], gr.update(value="")


with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown("""# 🌏💬 Chatbot TOEIC & Global Time-Weather 
      ## 📌 Introduction
      **TOEIC & Weather Chatbot** is an intelligent virtual assistant built with **LangChain + RAG + Agent**.  
      It can:
      - 📝 **Answer questions about the TOEIC exam in Vietnam**  
        Including: test format, registration locations, services, promotions, etc.
      - 🌦️ **Provide the current time & weather for cities around the world**  
        Just enter the city name (e.g., *Tokyo*, *New York*, *Hà Nội*) and the bot will respond with local time, weather conditions, temperature, and more.
      
      > **Note:** Please ask your questions in **Vietnamese** for the best results.""")


    chatbot = gr.Chatbot(
        label="Chatbot",
        height=420,
        # show_copy_button=True,   # cho phép copy nội dung nhanh
    )
    txt = gr.Textbox(
    placeholder="Nhập câu hỏi (Enter để gửi)...",
    submit_btn=True,
    scale=5,
    show_label=False
    )
        
    clear_btn = gr.Button("Clear", variant="secondary", scale=1)
    gr.Markdown("""|Example|
                    | --- | 
                    | Thời tiết Hà Nội lúc này?    | 
                    | Số điện thoại và email hỗ trợ khách hàng của kì thi TOEIC?|
    """)
    # State lịch sử hội thoại (list[tuple[str,str]])
    state = gr.State([])

    # Sự kiện gửi
    txt.submit(respond, inputs=[txt, state], outputs=[chatbot, txt]).then(
        lambda h: h, inputs=chatbot, outputs=state
    )

    # Nút clear
    clear_btn.click(clear_chat, outputs=[chatbot, txt]).then(
        lambda: [], outputs=state
    )

if __name__ == "__main__":
    demo.queue().launch(show_error=True, share=True)