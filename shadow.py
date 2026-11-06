# ==================================================
# 🌑 SHADOW — Website version (Streamlit)
# Run with Launch_SHADOW.bat  -> http://localhost:8501
# ==================================================

import streamlit as st
from pathlib import Path

from security import (detect_injection, read_file_safe, sanitize_filename,
                      validate_uploaded_file, SAFETY_CONFIG)
from shadow_core import ask_team, ollama_online, get_installed_models, AI_TEAM, resolve_model

st.set_page_config(page_title="SHADOW", page_icon="🌑", layout="centered")

# ─── Session state ───
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "🐬 Hi! SHADOW is ready. Ask me anything — I check with the team and pick the best answer."}
    ]
if "file_context" not in st.session_state:
    st.session_state.file_context = ""
if "seen_files" not in st.session_state:
    st.session_state.seen_files = set()

# ─── Sidebar ───
with st.sidebar:
    st.title("🌑 SHADOW")
    online = ollama_online()
    if online:
        st.success("Ollama: online ✅")
        installed = get_installed_models(refresh=True)
        with st.expander("Models"):
            for key, ai in AI_TEAM.items():
                st.write(f"{ai['name']} → `{resolve_model(ai['want'])}`")
            st.caption("Installed: " + (", ".join(installed) or "none"))
    else:
        st.error("Ollama: offline ❌\nOpen a terminal and run: ollama serve")

    st.divider()
    st.subheader("📎 Attach a file")
    up = st.file_uploader("Max %d MB" % SAFETY_CONFIG["max_file_size_mb"],
                          type=sorted(SAFETY_CONFIG["allowed_extensions"]))
    if up is not None and up.file_id not in st.session_state.seen_files:
        ok, msg = validate_uploaded_file(up)
        if not ok:
            st.error(msg)
        else:
            save_path = Path(SAFETY_CONFIG["upload_dir"]) / sanitize_filename(up.name)
            save_path.write_bytes(up.getbuffer())
            st.session_state.file_context = f"File: {up.name}\n" + read_file_safe(save_path)
            st.session_state.seen_files.add(up.file_id)
            st.success(f"Attached: {up.name}")
    if st.session_state.file_context:
        if st.button("Remove file"):
            st.session_state.file_context = ""
            st.rerun()

    if st.button("🧹 Clear chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# ─── Chat history ───
st.title("🌑 SHADOW")
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ─── New message ───
prompt = st.chat_input("Ask SHADOW...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if detect_injection(prompt):
            st.warning("⚠️ Suspicious input — processed with protection")
        with st.status("Thinking...", expanded=False) as status:
            history = [{"role": m["role"], "content": m["content"]}
                       for m in st.session_state.messages[1:-1]]
            answer = ask_team(prompt, history=history,
                              file_context=st.session_state.file_context,
                              on_status=lambda s: status.update(label=s))
            status.update(label="Done ✅", state="complete")
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})