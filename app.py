from openai import OpenAI
import streamlit as st

def main():
    with st.sidebar:
        openai_api_key = st.text_input("DS API Key", key="chatbot_api_key", type="password")

    st.title("💬 Chatbot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your DS API key to continue.")
            st.stop()

        client = OpenAI(api_key=openai_api_key, base_url="https://api.deepseek.com")
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # 创建占位符用于流式输出
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # 使用stream参数获取流式响应
            for chunk in client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages,
                stream=True
            ):
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
if __name__ == '__main__':
    main()