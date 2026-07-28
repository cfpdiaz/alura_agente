"""Aplicación Streamlit para el Agente Académico IA."""
import streamlit as st
from agent import AcademicAgent

st.set_page_config(
    page_title="Agente Académico IA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    .stChatMessage.user { background-color: #e3f2fd; }
    .stChatMessage.assistant { background-color: #f1f8e9; }
    .source-badge {
        display: inline-block;
        background-color: #e0e0e0;
        border-radius: 15px;
        padding: 3px 10px;
        margin: 2px;
        font-size: 0.8em;
    }
    .header { text-align: center; margin-bottom: 2rem; }
    .header h1 { color: #2c3e50; }
    .header p { color: #7f8c8d; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🎓 Agente Académico IA")
    st.markdown("---")
    st.markdown("### 📚 Temas disponibles")
    st.markdown("- Reglamento del Estudiante")
    st.markdown("- Política de Reembolso")
    st.markdown("- Preguntas Frecuentes")
    st.markdown("- Guía de Uso de la Plataforma")
    st.markdown("- Programa de Becas y Afiliados")
    st.markdown("- Horarios de Clases y Ramos")
    st.markdown("---")
    
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        if "agent" in st.session_state and st.session_state.agent:
            st.session_state.agent.clear_memory()
        st.rerun()

st.markdown("""
<div class="header">
    <h1>🎓 Agente Académico IA</h1>
    <p>Consulta sobre matrículas, horarios, becas, plataforma y reglamento estudiantil</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "¡Hola! Soy tu agente académico. Puedo ayudarte con consultas sobre matrículas, horarios, becas, uso de la plataforma online y el reglamento del estudiante. ¿En qué necesitas ayuda?"
    })

# Carga del agente leyendo el índice pre-compilado (es casi instantáneo)
if "agent" not in st.session_state:
    with st.spinner("Cargando base de conocimiento..."):
        try:
            st.session_state.agent = AcademicAgent()
            # Validamos si realmente se cargó la base de datos
            if st.session_state.agent.qa_chain:
                st.success("¡Agente listo! Puedes hacer tus consultas.")
            else:
                st.warning("⚠️ El agente arrancó pero no encontró el índice de documentos pre-cargado.")
        except Exception as e:
            st.error(f"Error al inicializar el agente: {str(e)}")
            st.session_state.agent = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.markdown("---")
            st.markdown("**Fuentes:**")
            for source in message["sources"]:
                st.markdown(
                    f'<span class="source-badge">{source["category"]}</span>',
                    unsafe_allow_html=True
                )

if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if st.session_state.get("agent"):
        with st.chat_message("assistant"):
            with st.spinner("Procesando consulta..."):
                try:
                    result = st.session_state.agent.query(prompt)
                    answer = result["answer"]
                    sources = result["sources"]
                    
                    st.markdown(answer)
                    if sources:
                        st.markdown("---")
                        st.markdown("**Fuentes consultadas:**")
                        for source in sources:
                            st.markdown(
                                f'<span class="source-badge">{source["category"]}</span>',
                                unsafe_allow_html=True
                            )
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    error_msg = f"❌ Error al procesar la consulta: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    else:
        with st.chat_message("assistant"):
            st.error("El agente no está disponible. Recarga la página.")
    
    st.rerun()
