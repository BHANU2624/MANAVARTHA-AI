import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000/search"

st.set_page_config(page_title="Telugu News Chatbot", page_icon="📰", layout="wide")

# --------------------- CSS ---------------------
st.markdown("""
<style>
.user {
    background-color: #1f6feb;
    color: white;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 0;
    max-width: 70%;
}
.bot {
    background-color: #033a16;
    color: #d1ffd6;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 0;
    max-width: 70%;
}
.sidebar-chat {
    padding: 10px;
    margin-bottom: 6px;
    border-radius: 6px;
    background-color: #161b22;
}
.sidebar-chat:hover {
    background-color: #1f6feb;
    color: white;
}
.chat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.delete-btn {
    color: #f54242;
    cursor: pointer;
}
.input-box {
    position: fixed;
    bottom: 0;
    left: 350px;
    right: 40px;
    padding: 15px;
    background-color: #161b22;
}
</style>
""", unsafe_allow_html=True)

# --------------------- SESSION STATE ---------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_chat" not in st.session_state:
    cid = str(uuid.uuid4())[:8]
    st.session_state.active_chat = cid
    st.session_state.chats[cid] = []

if "input_value" not in st.session_state:
    st.session_state.input_value = ""

# --------------------- SIDEBAR ---------------------
st.sidebar.title("💬 Conversations")

if st.sidebar.button("➕ New Chat"):
    nid = str(uuid.uuid4())[:8]
    st.session_state.active_chat = nid
    st.session_state.chats[nid] = []
    st.session_state.input_value = ""
    st.rerun()

# Show chat history list
for cid, messages in list(st.session_state.chats.items()):

    # Sidebar row
    with st.sidebar.container():
        col1, col2 = st.columns([4, 1])

        display_name = messages[0]["content"][:25] + "..." if messages else f"Chat {cid}"

        if col1.button(display_name, key=f"chat_{cid}"):
            st.session_state.active_chat = cid
            st.session_state.input_value = ""
            st.rerun()

        # Delete button
        if col2.button("🗑️", key=f"delete_{cid}"):
            del st.session_state.chats[cid]
            if st.session_state.active_chat == cid:
                # switch to a new chat
                new_id = str(uuid.uuid4())[:8]
                st.session_state.active_chat = new_id
                st.session_state.chats[new_id] = []
            st.rerun()

# --------------------- MAIN CHAT DISPLAY ---------------------
active_id = st.session_state.active_chat
chat = st.session_state.chats[active_id]

st.title("📰 Telugu News Q&A Chatbot")

chat_area = st.container()

with chat_area:
    for msg in chat:
        if msg["role"] == "user":
            st.markdown(f"<div class='user'><b>🧑 You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot'><b>🤖 Bot:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# --------------------- INPUT BOX ---------------------
st.markdown("<div class='input-box'>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_message = st.text_input("Ask your question…", value=st.session_state.input_value)
    submitted = st.form_submit_button("📨 Send")

st.markdown("</div>", unsafe_allow_html=True)

# --------------------- HANDLE SUBMISSION ---------------------
if submitted and user_message.strip():

    # ADD USER MESSAGE IMMEDIATELY (fixes delay)
    st.session_state.chats[active_id].append({"role": "user", "content": user_message})

    # Save cleared input
    st.session_state.input_value = ""

    # CALL API
    try:
        # Using GET request with query parameter as per backend
        r = requests.get(API_URL, params={"query": user_message})
        if r.status_code == 200:
            answer = r.json().get("answer", "No answer.")
        else:
             answer = f"API Error ({r.status_code}): {r.text}"
    except Exception as e:
        answer = f"API Error: {str(e)}"

    # Add bot message
    st.session_state.chats[active_id].append({"role": "bot", "content": answer})

    st.rerun()
