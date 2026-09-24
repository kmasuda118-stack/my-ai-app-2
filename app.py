import streamlit as st
from openai import OpenAI

st.title("🤖 マイAIアシスタント")

# ファイルから知識を読み込む
try:
    with open("my_knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()
except FileNotFoundError:
    knowledge = "（まだメモがありません）"

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージを表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ユーザーからの入力
if prompt := st.chat_input("質問を入力してください"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの回答生成
    with st.chat_message("assistant"):
        client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        
        system_prompt = f"以下の知識を参考に質問に答えてください:\n{knowledge}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
