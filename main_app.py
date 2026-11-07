import streamlit as st
from pathlib import Path
import scan_engine  # connects to File 2

# ─── Page Setup ───
st.set_page_config(page_title="🌑 ECLIPSED", layout="wide")
st.title("🌑 ECLIPSED — Your Personal File Assistant")
st.divider()

# ─── Memory ───
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── Choose What To Do ───
tab1, tab2 = st.tabs(["💬 Ask About Files", "📂 Scan Folder First"])

with tab1:
    st.subheader("Ask ECLIPSED")
    
    # Where to search
    search_folder = st.text_input(
        "📁 Search in this folder:",
        value=str(Path.home()),
        help="Example: C:\\Users\\sin hu hai\\Documents"
    )
    
    # Your question
    user_question = st.text_area("❓ Your question:", placeholder="What do you want to find in your files?")
    
    # Search button
    if st.button("🚀 Search & Answer", type="primary") and user_question:
        with st.spinner("Scanning your files... please wait..."):
            # Call the scan engine
            results = scan_engine.search_and_answer(search_folder, user_question)
            
            # Save to chat
            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("ECLIPSED", results))
    
    # Show conversation
    st.divider()
    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.info(f"👤 You: {msg}")
        else:
            st.success(f"🌑 ECLIPSED:\n{msg}")

with tab2:
    st.subheader("List All Files in Folder")
    list_folder = st.text_input(
        "📂 Folder to scan:",
        value=str(Path.home()),
        key="list_folder"
    )
    include_sub = st.checkbox("Include subfolders", value=True)
    
    if st.button("📋 List Files"):
        file_list = scan_engine.get_all_files(list_folder, include_sub)
        st.write(f"Found **{len(file_list)}** file(s):")
        for f in file_list[:200]:  # Show first 200
            st.write(f"📄 {f}")
        if len(file_list) > 200:
            st.write(f"...and {len(file_list)-200} more files")

st.caption("🌑 ECLIPSED — All local • All yours • No limits")
