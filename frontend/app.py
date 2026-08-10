import streamlit as st

from utils import call_health, call_query, call_root, call_upload

st.set_page_config(page_title="AI SIP Log Analyser", layout="wide")
st.title("AI Based SIP Call Log Analyser")

RESPONSE_KEYS = [
    "root_response",
    "health_response",
    "upload_response",
    "query_response",
]


def clear_responses():
    for key in RESPONSE_KEYS:
        st.session_state.pop(key, None)


# --- Sidebar ---
with st.sidebar:
    st.header("Backend")
    st.caption("Configured via BACKEND_URL env var")

    st.divider()

    st.subheader("1. Service Checks")
    if st.button("Root Check"):
        clear_responses()
        try:
            st.session_state.root_response = call_root()
        except Exception as e:
            st.session_state.root_response = {"error": str(e)}

    if st.button("Health Check"):
        clear_responses()
        try:
            st.session_state.health_response = call_health()
        except Exception as e:
            st.session_state.health_response = {"error": str(e)}

    st.divider()

    st.subheader("2. Upload Log File")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "log"])
    if st.button("Upload File") and uploaded_file:
        clear_responses()
        try:
            file_type = uploaded_file.type if uploaded_file.type else "text/plain"
            status, resp = call_upload(uploaded_file, file_type)
            if status == 200:
                st.session_state.uploaded_file_path = resp.get("path")
                st.session_state.upload_response = resp
                st.success("Uploaded successfully")
            else:
                st.error(f"Upload failed: {resp.get('detail')}")
        except Exception as e:
            st.error(f"Backend unreachable: {e}")

    if st.session_state.get("uploaded_file_path"):
        st.caption(f"Active file: `{st.session_state.uploaded_file_path}`")

    st.divider()

    st.subheader("3. Query")
    query_text = st.text_area("Enter your query")
    if st.button("Ask AI"):
        if not st.session_state.get("uploaded_file_path"):
            st.warning("Upload a file first")
        elif not query_text.strip():
            st.warning("Enter a query")
        else:
            clear_responses()
            try:
                status, resp = call_query(
                    query_text, st.session_state.uploaded_file_path
                )
                if status == 200:
                    st.session_state.query_response = resp
                else:
                    st.error(f"Query failed: {resp.get('detail')}")
            except Exception as e:
                st.error(f"Backend unreachable: {e}")


# --- Main Area ---
if st.session_state.get("root_response"):
    st.subheader("Root Response")
    st.json(st.session_state.root_response)

if st.session_state.get("health_response"):
    st.subheader("Health Status")
    st.json(st.session_state.health_response)

if st.session_state.get("upload_response"):
    st.subheader("Upload Result")
    st.json(st.session_state.upload_response)

if st.session_state.get("query_response"):
    resp = st.session_state.query_response
    st.subheader("AI Answer")
    st.write(resp.get("answer"))
    with st.expander("Sources"):
        st.write(resp.get("sources"))
    st.caption(f"Latency: {resp.get('latency_ms')} ms")
