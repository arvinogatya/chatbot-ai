import os

import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) 

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel()


def handle_user_query(msg, chatbot):
    print(msg, chatbot) 
    chatbot += [[msg, None]]
    return '', chatbot

def generate_chatbot(chatbot: list[list[str, str]]) -> list[list[str, str]]:
    formatted_chatbot = []
    if len(chatbot) == 0:
        return formatted_chatbot
    for ch in chatbot:
        formatted_chatbot.append(
            {
                "role": "user",
                "parts": [ch[0]]
            }
        )
        formatted_chatbot.append(
            {
                "role": "model",
                "parts": [ch[1]]
            }
        )

def handle_gemini_response(chatbot):
    query = chatbot[-1][0]
    print(chatbot)
    formatted_chatbot = generate_chatbot(chatbot[:-1])
    print(formatted_chatbot)
    chat = model.start_chat(history=formatted_chatbot)
    response = chat.send_message(query)
    chatbot[-1][1] = response.text
    return chatbot


custom_css = """
body {
    background: #1e1e2f;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
header {
    background: #6c63ff;
    color: white;
    font-size: 1.5rem;
    font-weight: 700;
    text-align: center;
    padding: 16px;
    box-shadow: 0 3px 10px rgba(108, 99, 255, 0.5);
}
#chatbox {
    background: #2c2c43;
    padding: 12px;
}
.message.user {
    background: #6c63ff;
    color: white;
    align-self: flex-end;
    border-radius: 20px 20px 4px 20px;
}
.message.ai {
    background: #464677;
    color: #ddd;
    align-self: flex-start;
    border-radius: 20px 20px 20px 4px;
}
.gr-button {
    background: #6c63ff;
    border-radius: 24px;
    font-weight: 600;
}
.gr-button:hover {
    background: #574fd6;
}
"""


with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:
    gr.HTML("<header>VIUU AI Chatbot</header>")
    chatbot = gr.Chatbot(elem_id="chatbox", show_label=False)
    state = gr.State([])
    )
    with gr.Row():
        txt = gr.Textbox(
            show_label=False,
            placeholder="Type your message...",
            container=True,
            scale=8
        )
        send_btn = gr.Button("Send", scale=2)

    def respond(history, user_input):
        return chatbot(history, user_input)

    send_btn.click(respond, [state, txt], [chatbot, txt])
    txt.submit(respond, [state, txt], [chatbot, txt])

    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        handle_gemini_response,
        [chatbot],
        [chatbot]
    )
       
if __name__ == "__main__":
    demo.queue()
    demo.launch()