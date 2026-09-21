"""A small Streamlit chat simulator for deployment testing. Testing"""

from collections.abc import Iterator

import streamlit as st


def create_response(user_message: str) -> str:
    """Create a deterministic local response without calling an AI service."""
    return f'Test chat reply: You said, "{user_message.strip()}"'


def stream_response(response: str) -> Iterator[str]:
    """Yield a response one word at a time for the chat UI."""
    words = response.split()
    for index, word in enumerate(words):
        separator = " " if index < len(words) - 1 else ""
        yield f"{word}{separator}"


def main() -> None:
    """Render the Streamlit chat application."""
    st.set_page_config(page_title="Test Chat", page_icon="💬")
    st.title("Test Chat")
    st.caption("A local chat simulator for Azure deployment testing.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.sidebar.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_message := st.chat_input("Type a message"):
        st.session_state.messages.append(
            {"role": "user", "content": user_message}
        )
        with st.chat_message("user"):
            st.markdown(user_message)

        response = create_response(user_message)
        with st.chat_message("assistant"):
            displayed_response = st.write_stream(stream_response(response))

        st.session_state.messages.append(
            {"role": "assistant", "content": displayed_response}
        )


if __name__ == "__main__":
    main()
