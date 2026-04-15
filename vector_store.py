import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

# Load the secret API key from the .env file
load_dotenv()

class VectorWarehouse:
    def __init__(self):
        # We use Google's latest embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.db_path = "faiss_index"
        self.vector_store = None

        # If a database already exists on your hard drive, load it. 
        # Otherwise, start fresh.
        if os.path.exists(self.db_path):
            # allow_dangerous_deserialization is required for local FAISS loading in newer versions
            self.vector_store = FAISS.load_local(self.db_path, self.embeddings, allow_dangerous_deserialization=True)
            print("📚 Loaded existing Vector Database.")
        else:
            print("🆕 No existing database found. Starting fresh.")

    def memorize(self, chunks):
        """Converts text chunks into vectors and saves them to the database."""
        if not chunks:
            return

        # Convert our dictionary chunks into LangChain 'Document' objects
        docs = [Document(page_content=c["text"], metadata=c["metadata"]) for c in chunks]
        
        print("🧠 Generating embeddings and updating FAISS index...")
        
        if self.vector_store is None:
            # Create a brand new index
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
        else:
            # Append to the existing index
            self.vector_store.add_documents(docs)
            
        # Save the updated database back to the hard drive!
        self.vector_store.save_local(self.db_path)
        print(f"💾 Successfully memorized {len(chunks)} chunks into local storage.")