from openai import OpenAI
import streamlit as st

# Configure sua chave API do OpenAI
client = OpenAI(api_key='sk-07_o65ohhXGEwCKJiq8Lj_6h7VAYjmSZplLjN0tmEJT3BlbkFJEU-9pJMLpgqhHZvK_4R_W_dGNajsu5AElC4CjK6dYA')

def chat_with_gpt4o(start_message, chat_log=None):
    chat_log = chat_log or []
    messages = [
        {"role": "system", "content": "Você é um assistente de entrevistas de emprego."},
        {"role": "user", "content": start_message}
    ] + chat_log

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    
    return response.choices[0].message.content, messages

def main():
    st.title("Simulador de Entrevistas de Emprego")
    vaga = st.text_input("Digite a vaga para a qual está se preparando:")

    if vaga:
        st.session_state['chat_log'] = st.session_state.get('chat_log', [])
        st.session_state['chat_log'].append({"role": "user", "content": f"Entrevista para a vaga de {vaga}"})
        
        pergunta, chat_log = chat_with_gpt4o(f"Entrevista para a vaga de {vaga}", st.session_state['chat_log'])
        st.session_state['chat_log'] = chat_log
        st.write(f"Pergunta: {pergunta}")

        resposta = st.text_area("Sua resposta:")
        if st.button("Enviar Resposta"):
            st.session_state['chat_log'].append({"role": "user", "content": resposta})
            feedback, chat_log = chat_with_gpt4o(resposta, st.session_state['chat_log'])
            st.session_state['chat_log'] = chat_log
            st.write("Feedback:", feedback)

if __name__ == "__main__":
    main()
