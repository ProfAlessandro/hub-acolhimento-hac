import streamlit as st
import whisper
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import os

# Configuração de Layout e Tema da Página
st.set_page_config(page_title="HAC - Hub de Acolhimento", page_icon="🚀", layout="centered")

# Inicialização da Inteligência Artificial em Cache de Memória
@st.cache_resource
def carregar_modelo_ia():
    print("🧠 Carregando modelo Whisper em segundo plano...")
    # O Streamlit Cloud possui 1GB de RAM, aguentando o modelo 'tiny' com folga!
    return whisper.load_model("tiny")

modelo_transcricao = carregar_modelo_ia()

# TÍTULO E INTERFACE DO APLICATIVO
st.title("🚀 Hub de Acolhimento e Comunicação - HAC")
st.markdown("### Tradução Multiuso em Tempo Real para Acolhimento de Estudantes Latinos")

# ÁREA DE ENTRADA DE DADOS (Opção A e Opção B)
entrada_texto = st.text_area("Opção A: Digite em português:", placeholder="Escreva o aviso, recado ou conversa aqui...", height=100)

# Componente nativo de microfone do Streamlit (Grava direto da tela sem apps externos)
entrada_audio = st.audio_input("Opção B: Áudio (Clique no microfone abaixo para falar):")

# BOTÕES DE AÇÃO DO SISTEMA
col1, col2 = st.columns(2)
with col1:
    botao_traduzir = st.button("✨ Traduzir", type="primary", use_container_width=True)
with col2:
    botao_limpar = st.button("🧹 Limpar Dados", type="secondary", use_container_width=True)

# LÓGICA DE PROCESSAMENTO (BACK-END EM PYTHON)
if botao_traduzir:
    texto_final_pt = ""
    
    # REGRA DE PRIORIDADE: Se houver gravação no microfone nativo
    if entrada_audio is not None:
        st.info("🎙️ Priorizando áudio capturado pelo microfone...")
        # Salva o arquivo temporário enviado pelo navegador para o Whisper ler
        with open("audio_temp.wav", "wb") as f:
            f.write(entrada_audio.getbuffer())
        
        resultado_transcricao = modelo_transcricao.transcribe("audio_temp.wav", language="pt")
        texto_final_pt = resultado_transcricao["text"]
    else:
        texto_final_pt = entrada_texto

    # Validação de Segurança
    if not texto_final_pt or not texto_final_pt.strip():
        st.warning("⚠️ Por favor, digite um texto ou grave seu áudio antes de clicar em Traduzir.")
    else:
        # Tradução instantânea em tempo real via MyMemory
        texto_espanhol = MyMemoryTranslator(source='pt-BR', target='es-ES').translate(texto_final_pt)
        
        # Síntese de voz em espanhol por IA
        IA_voz = gTTS(text=texto_espanhol, lang='es', slow=False)
        nome_arquivo = "traducao_hac.mp3"
        IA_voz.save(nome_arquivo)
        
        # EXIBIÇÃO DOS RESULTADOS NA TELA
        st.success("✅ Processamento concluído com sucesso!")
        
        st.text_input("📝 Texto Identificado (Português):", value=texto_final_pt, disabled=True)
        st.text_input("🔄 Tradução Automática (Espanhol):", value=texto_espanhol, disabled=True)
        
        st.markdown("##### 🔊 Pronúncia da IA (Espanhol Nativo):")
        st.audio(nome_arquivo, format="audio/mp3", autoplay=True)

# LÓGICA DO BOTÃO LIMPAR (Usa o recarregamento nativo do Streamlit)
if botao_limpar:
    st.rerun()

# RODAPÉ E CRÉDITOS DE DESENVOLVEDOR
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>🛠️ <b>Desenvolvido por: Professor Alessandro Ramos e Gemini</b><br><i>Projeto de Inclusão Tecnológica e Social com Inteligência Artificial e Python</i></p>", 
    unsafe_allow_html=True
)
