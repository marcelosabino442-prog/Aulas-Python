
import streamlit as st

# Configuração da página do aplicativo
st.set_page_config(
    page_title="Minha Lista de Tarefas", page_icon="📝", layout="centered"
)

# Estilização visual personalizada (Cores e fontes)
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
    }
    .stCheckbox {
        font-size: 18px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Título do App
st.markdown("<h1>📝 Meu App de Tarefas</h1>", unsafe_allow_html=True)
st.write(
    "Organize seu dia de forma simples e rápida! Adicione, marque como concluídas ou remova suas tarefas."
)

# Inicializar a lista de tarefas na memória do aplicativo (Session State)
if "tarefas" not in st.session_state:
    st.session_state.tarefas = []

# Campo para digitar uma nova tarefa
with st.form(key="form_tarefa", clear_on_submit=True):
    nova_tarefa = st.text_input(
        "O que você precisa fazer?", placeholder="Ex: Estudar Python às 15h"
    )
    botao_adicionar = st.form_submit_button(label="Adicionar Tarefa")

    if botao_adicionar and nova_tarefa:
        st.session_state.tarefas.append(
            {"texto": nova_tarefa, "concluida": False}
        )
        st.success(f"Tarefa '{nova_tarefa}' adicionada com sucesso!")

# Exibir e gerenciar a lista de tarefas
if st.session_state.tarefas:
    st.markdown("---")
    st.subheader("Suas Tarefas:")

    for i, tarefa in enumerate(st.session_state.tarefas):
        col1, col2 = st.columns([0.8, 0.2])

        with col1:
            # Checkbox para marcar como concluída (com risco no texto se feito)
            concluida = st.checkbox(
                tarefa["texto"],
                value=tarefa["concluida"],
                key=f"check_{i}",
            )
            st.session_state.tarefas[i]["concluida"] = concluida

        with col2:
            # Botão para excluir a tarefa individualmente
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.tarefas.pop(i)
                st.rerun()

    # Botão para limpar todas as tarefas concluídas
    if st.sum([t["concluida"] for t in st.session_state.tarefas]) > 0:
        if st.button("Limpar Concluídas"):
            st.session_state.tarefas = [
                t for t in st.session_state.tarefas if not t["concluida"]
            ]
            st.rerun()
else:
    st.info("Sua lista está vazia. Adicione uma tarefa acima para começar!")