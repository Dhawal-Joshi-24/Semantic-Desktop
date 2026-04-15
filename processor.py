import os
import fitz  # PyMuPDF
from vector_store import VectorWarehouse
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
       self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            length_function=len,
        )
        # Add the warehouse connection here!
       self.warehouse = VectorWarehouse()

    def extract_text(self, file_path):
        """Identifies the file type and extracts the text accordingly."""
        extension = os.path.splitext(file_path)[1].lower()
        text = ""

        try:
            if extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            
            elif extension == '.pdf':
                # Open the PDF and extract text page by page
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text()
                doc.close()
            
            else:
                print(f"⚠️ Unsupported file format: {extension}")
                return None
                
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return None

        return text

    def process_file(self, file_path):
        """The main pipeline: Read -> Chunk -> Add Metadata"""
        print(f"⚙️ Processing: {file_path}")
        
        # 1. Extract the raw text
        raw_text = self.extract_text(file_path)
        if not raw_text or len(raw_text.strip()) == 0:
            print("No text found or file empty.")
            return None

        # 2. Chop into manageable pieces (Chunks)
        chunks = self.text_splitter.split_text(raw_text)

        # 3. Attach Metadata to every chunk
        # If the AI finds a chunk, we need to know exactly which file it came from!
        processed_chunks = []
        for i, chunk_text in enumerate(chunks):
            chunk_data = {
                "text": chunk_text,
                "metadata": {
                    "source": file_path,
                    "chunk_id": i,
                    "file_type": os.path.splitext(file_path)[1].lower()
                }
            }
            processed_chunks.append(chunk_data)

        print(f"✅ Successfully created {len(processed_chunks)} chunks for {file_path}")
        self.warehouse.memorize(processed_chunks)
        return processed_chunks

# Quick test if you run this file directly
if __name__ == "__main__":
    # Create a dummy file to test
    test_file = "test_doc.txt"
    with open(test_file, "w") as f:
        f.write("This is a test document. " * 100) # Creating a long string
        
    processor = DocumentProcessor()
    results = processor.process_file(test_file)
    print(f"First chunk preview: {results[0]['text'][:50]}...")