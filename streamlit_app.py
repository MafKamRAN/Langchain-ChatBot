import streamlit as st
from chatbot import ChatBot, get_available_models, HumanMessage, AIMessage

# Page config
st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBot()
if "models_loaded" not in st.session_state:
    st.session_state.models = get_available_models()
    st.session_state.models_loaded = True

# Sidebar - Settings
with st.sidebar:
    st.header("Settings")

    # Model selection
    st.subheader("Model")
    model_index = 0
    if st.session_state.chatbot.model in st.session_state.models:
        model_index = st.session_state.models.index(st.session_state.chatbot.model)

    selected_model = st.selectbox(
        "Select Model",
        st.session_state.models,
        index=model_index
    )

    # Temperature
    st.subheader("Temperature")
    temperature = st.slider(
        "Response creativity",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.chatbot.temperature,
        step=0.1
    )

    # Max turns
    st.subheader("Max Turns")
    max_turns = st.slider(
        "Conversation limit",
        min_value=1,
        max_value=20,
        value=st.session_state.chatbot.max_turns
    )

    # System prompt
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Instructions",
        value=st.session_state.chatbot.system_prompt,
        height=100
    )

    st.divider()

    # Apply button
    if st.button("Apply Settings", type="primary"):
        st.session_state.chatbot.update_settings(
            model=selected_model,
            temperature=temperature,
            max_turns=max_turns,
            system_prompt=system_prompt
        )
        st.success("Settings applied!")

    # Clear button
    if st.button("Clear Chat"):
        st.session_state.chatbot.reset_history()
        st.rerun()

    st.divider()

    # Status info
    st.subheader("Status")
    st.text(f"Model: {st.session_state.chatbot.model}")
    st.text(f"Temperature: {st.session_state.chatbot.temperature}")
    st.text(f"Turns: {len(st.session_state.chatbot.chat_history) // 2}/{st.session_state.chatbot.max_turns}")

    # Refresh models
    if st.button("Refresh Models"):
        st.session_state.models = get_available_models()
        st.rerun()

# Main area
st.title("LangChain Chatbot")
st.caption(f"Model: {st.session_state.chatbot.model} | Max turns: {st.session_state.chatbot.max_turns}")

# Display chat history
for message in st.session_state.chatbot.chat_history:
    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Display user message
    st.chat_message("user").write(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, _ = st.session_state.chatbot.chat(prompt)
            st.write(response)

            # Warnings
            if "turn(s) left" in response:
                st.warning("Approaching turn limit")
            if "Context window is full" in response:
                st.error("Context limit reached - clear chat to continue")
