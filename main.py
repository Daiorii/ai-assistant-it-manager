import os
import customtkinter as ctk
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# ТЕМА
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# =========================
# GEMINI API
# =========================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("GEMINI_API_KEY не найден")
    exit()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

# =========================
# ЧАТЫ
# =========================

chats = {}
current_chat = None

# =========================
# СОЗДАТЬ ЧАТ
# =========================

def create_new_chat():

    global current_chat

    chat_name = f"Чат {len(chats) + 1}"

    chats[chat_name] = []

    current_chat = chat_name

    add_chat_button(chat_name)

    load_chat(chat_name)

# =========================
# КНОПКА ЧАТА
# =========================

def add_chat_button(chat_name):

    button = ctk.CTkButton(
        history_frame,
        text=chat_name,
        width=220,
        height=45,
        corner_radius=14,
        fg_color="#1f1f1f",
        hover_color="#333333",
        anchor="w",
        font=("Arial", 15),
        command=lambda: load_chat(chat_name)
    )

    button.pack(
        pady=5,
        padx=10,
        fill="x"
    )

# =========================
# ЗАГРУЗКА ЧАТА
# =========================

def load_chat(chat_name):

    global current_chat

    current_chat = chat_name

    answer_box.configure(state="normal")

    answer_box.delete("1.0", "end")

    for message in chats[chat_name]:

        answer_box.insert(
            "end",
            message + "\n\n"
        )

    answer_box.configure(state="disabled")

# =========================
# AI RESPONSE
# =========================

def get_ai_response(question):

    global current_chat

    try:

        response = model.generate_content(question)

        ai_answer = response.text

    except Exception:

        ai_answer = """
Gemini API временно недоступен
или превышен лимит запросов.
"""

    chats[current_chat].append(
        f"🧑 Вы:\n{question}"
    )

    chats[current_chat].append(
        f"🤖 AI:\n{ai_answer}"
    )

    load_chat(current_chat)

# =========================
# ОТПРАВКА
# =========================

def ask_ai():

    global current_chat

    question = input_box.get().strip()

    if question == "":
        return

    if current_chat is None:
        create_new_chat()

    get_ai_response(question)

    input_box.delete(0, "end")

# =========================
# ENTER = SEND
# =========================

def enter_send(event):

    ask_ai()

# =========================
# ОЧИСТКА
# =========================

def clear_chat():

    global current_chat

    if current_chat:

        chats[current_chat] = []

        load_chat(current_chat)

# =========================
# APP
# =========================

app = ctk.CTk()

app.title("AI Assistant")

app.geometry("1450x850")

app.configure(
    fg_color="#000000"
)

# =========================
# SIDEBAR
# =========================

sidebar = ctk.CTkFrame(
    app,
    width=290,
    fg_color="#0d0d0d",
    corner_radius=0
)

sidebar.pack(
    side="left",
    fill="y"
)

# =========================
# LOGO
# =========================

logo = ctk.CTkLabel(
    sidebar,
    text="AI Assistant",
    font=("Arial", 30, "bold"),
    text_color="white"
)

logo.pack(
    pady=(30, 25)
)

# =========================
# NEW CHAT
# =========================

new_chat_button = ctk.CTkButton(
    sidebar,
    text="+ Новый чат",
    width=230,
    height=50,
    corner_radius=18,
    fg_color="#2b2b2b",
    hover_color="#3b3b3b",
    text_color="white",
    font=("Arial", 16, "bold"),
    command=create_new_chat
)

new_chat_button.pack(
    pady=10
)

# =========================
# HISTORY TEXT
# =========================

history_text = ctk.CTkLabel(
    sidebar,
    text="История",
    text_color="gray",
    font=("Arial", 16)
)

history_text.pack(
    pady=(30, 10)
)

# =========================
# HISTORY FRAME
# =========================

history_frame = ctk.CTkScrollableFrame(
    sidebar,
    width=250,
    fg_color="#0d0d0d",
    scrollbar_button_color="#444444",
    scrollbar_button_hover_color="#666666"
)

history_frame.pack(
    expand=True,
    fill="both",
    padx=10,
    pady=(0, 15)
)

# =========================
# MAIN FRAME
# =========================

main_frame = ctk.CTkFrame(
    app,
    fg_color="#000000"
)

main_frame.pack(
    side="right",
    expand=True,
    fill="both"
)

# =========================
# TITLE
# =========================

title = ctk.CTkLabel(
    main_frame,
    text="AI Assistant for IT Managers",
    text_color="white",
    font=("Arial", 36, "bold")
)

title.pack(
    pady=(35, 10)
)

# =========================
# SUBTITLE
# =========================

subtitle = ctk.CTkLabel(
    main_frame,
    text="Интеллектуальный помощник",
    text_color="gray",
    font=("Arial", 17)
)

subtitle.pack(
    pady=(0, 20)
)

# =========================
# ANSWER BOX
# =========================

answer_box = ctk.CTkTextbox(
    main_frame,
    width=930,
    height=520,
    corner_radius=28,
    fg_color="#111111",
    border_width=1,
    border_color="#2d2d2d",
    text_color="white",
    font=("Arial", 17),

    scrollbar_button_color="#444444",
    scrollbar_button_hover_color="#666666"
)

answer_box.pack(
    pady=20
)

answer_box.configure(
    state="disabled"
)

# =========================
# INPUT FRAME
# =========================

input_frame = ctk.CTkFrame(
    main_frame,
    width=980,
    height=85,
    corner_radius=30,
    fg_color="#111111",
    border_width=1,
    border_color="#2d2d2d"
)

input_frame.pack(
    pady=(10, 15)
)

input_frame.pack_propagate(False)

# =========================
# INPUT BOX
# =========================

input_box = ctk.CTkEntry(
    input_frame,

    width=820,
    height=50,

    corner_radius=20,

    fg_color="#111111",

    border_width=0,

    text_color="white",

    placeholder_text="Введите запрос...",

    placeholder_text_color="gray",

    font=("Arial", 17)
)

input_box.pack(
    side="left",
    padx=(20, 10),
    pady=17
)

input_box.focus()

input_box.bind(
    "<Return>",
    enter_send
)

# =========================
# SEND BUTTON
# =========================

send_button = ctk.CTkButton(
    input_frame,
    text="↑",
    width=55,
    height=55,
    corner_radius=100,
    fg_color="#2c2c2c",
    hover_color="#3c3c3c",
    text_color="white",
    font=("Arial", 24, "bold"),
    command=ask_ai
)

send_button.pack(
    side="right",
    padx=15
)

# =========================
# CLEAR BUTTON
# =========================

clear_button = ctk.CTkButton(
    main_frame,
    text="Очистить чат",
    width=200,
    height=45,
    corner_radius=18,
    fg_color="#1f1f1f",
    hover_color="#333333",
    text_color="white",
    font=("Arial", 15),
    command=clear_chat
)

clear_button.pack()

# =========================
# START
# =========================

app.mainloop()