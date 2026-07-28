"""Script para pre-procesar los documentos y generar el índice FAISS offline."""
import os
from agent.config import Config
from agent.document_processor import DocumentProcessor
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Cargar API_KEY del archivo .env local
load_dotenv()

def build_and_save_index():
    config = Config()
    
    if not config.GOOGLE_API_KEY:
        print("⚠️ ERROR: No se encontró GOOGLE_API_KEY en las variables de entorno.")
        print("Asegúrate de configurarla en tu archivo .env antes de ejecutar este script.")
        return

    print("⚙️ Leyendo documentos desde la carpeta 'data/'...")
    processor = DocumentProcessor(config)
    
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Carpeta 'data' creada. Coloca tus archivos .docx allí y vuelve a ejecutar.")
        return
        
    documents = processor.process_documents("data")
    
    if not documents:
        print("❌ No se encontraron documentos .docx para procesar.")
        return
        
    print(f"✅ Se generaron {len(documents)} fragmentos (chunks) de texto.")
    print("🚀 Conectando con Google Gemini para generar embeddings... (Esto tomará unos segundos)")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    # Aquí se hace la llamada pesada a la API que generaba el Error 504
    vector_store = FAISS.from_documents(documents, embeddings)
    
    print(f"💾 Guardando índice vectorial en la carpeta '{config.FAISS_INDEX_PATH}'...")
    vector_store.save_local(config.FAISS_INDEX_PATH)
    print("🎉 ¡Índice creado exitosamente! Ahora debes subir LA CARPETA COMPLETA ('faiss_index') a GitHub.")

if __name__ == "__main__":
    build_and_save_index()
