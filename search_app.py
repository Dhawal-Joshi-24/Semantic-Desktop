import streamlit as st
import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load your secret API key
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# --- UI Setup ---
st.set_page_config(page_title="Semantic Desktop", page_icon="🧠")
st.title("🧠 AI Semantic Desktop")
st.caption("A local RAG search engine for your private files.")

@st.cache_resource
def load_brain():
    """Loads the database into memory only once to keep the app fast."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    if os.path.exists("faiss_index"):
        return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return None

vector_store = load_brain()

if vector_store is None:
    st.warning("No database found. Please run your Watcher and drop some files into 'my_documents' first!")
else:
    # 1. The Search Bar
    user_question = st.text_input("Ask a question about your files:")
    
    if user_question:
        with st.spinner("Searching your local files..."):
            
            # 2. Retrieve the relevant chunks from FAISS
            retrieved_docs = vector_store.similarity_search(user_question, k=4)
            
            # 3. MANUAL RAG ASSEMBLY
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            
            strict_prompt = f"""
            You are an AI assistant helping a user find information in their personal files.
            Answer the user's question ONLY using the context provided below. 
            If the answer is not in the context, say "I cannot find this in your documents."
            
            Context:
            {context}
            
            Question:
            {user_question}
            """
            
            # 4. Auto-Discover the Model (The Bulletproof Method)
            # Ask Google what models this specific API key is allowed to use
            available_models = [
                m.name for m in genai.list_models() 
                if 'generateContent' in m.supported_generation_methods
            ]
            
            # Prioritize Gemini 1.5 Flash, then fallback to Pro
            target_model = None
            for m in available_models:
                if "1.5-flash" in m:
                    target_model = m
                    break
                    
            if not target_model: # Fallback loop
                for m in available_models:
                    if "gemini-pro" in m:
                        target_model = m
                        break
            
            if target_model:
                st.info(f"Dynamically routed to model: `{target_model}`")
                model = genai.GenerativeModel(target_model)
                response = model.generate_content(strict_prompt)
                
                # 5. Display the Answer
                st.markdown("### Answer:")
                st.write(response.text)
            else:
                st.error(f"No generation models available for this API key. Allowed models: {available_models}")
            
            # 6. Prove it's not lying
            st.markdown("---")
            with st.expander("📄 View Source Documents"):
                for i, doc in enumerate(retrieved_docs):
                    st.write(f"**Source {i+1}:** `{doc.metadata['source']}` (Chunk ID: {doc.metadata['chunk_id']})")
                    st.caption(f"_{doc.page_content[:200]}..._")