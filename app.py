import streamlit as st
import fitz  # PyMuPDF
import io 
from PIL import Image
import pytesseract
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter

st.title("Document Information Extraction")

upload_file = st.file_uploader("Upload documents", type=["pdf", "png", "jpg", "jpeg", "txt"], accept_multiple_files = rue)

def chunk_text(text, chunk_size = 1000, chunk_overlap = 200):
    if not text.strip():
        return []
    splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    return splitter.split_text(text)

def extract_text_from_pdf(file):
    file.seek(0)  # Reset file pointer
    doc = fitz.open(stream=file.read(), filetype = "pdf")
    chunks = []
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        if text.strip():
            for chunk in chunk_text(text):
                chunks.append({
                    "doc_id": str(uuid.uuid4())[:8],
                    "page": page_num + 1,
                    "text": chunk
                })
    doc.close()
    return chunks

def extract_text_from_image(file):
    file.seek(0)
    image = Image.open(io.BytesIO(file.read()))
    text = pytesseract.image_to_string(image)
    chunks = []
    
    for chunk in chunk_text(text):
        chunks.append({
            "doc_id": str(uuid.uuid4())[:8],
            "page": None,
            "text": chunk
        })
    return chunks

def extract_text_from_txt(file):
    file.seek(0)
    text = file.read().decode("utf-8")
    chunks = []
    
    for chunk in chunk_text(text):
        chunks.append({
            "doc_id": str(uuid.uuid4())[:8],
            "page": None,
            "text": chunk
        })
    return chunks

if upload_file:
    all_chunks = []
    st.subheader("Extracted Document Content")

    for file in upload_file:
        st.markdown(f"#### {file.name}")
        file_type = file.name.split(".")[-1].lower()

        try:
            if file_type == "pdf":
                chunks = extract_text_from_pdf(file)
            elif file_type in ["png", "jpg", "jpeg"]:
                chunks = extract_text_from_image(file)
            elif file_type == "txt":
                chunks = extract_text_from_txt(file)
            else:
                st.error("Unsupported file type!")
                continue

            # Show first 3 chunks
            for chunk in chunks[:3]:
                st.code(f"[Doc ID: {chunk['doc_id']}, Page: {chunk['page']}]\n{chunk['text']}")

            all_chunks.extend(chunks)
            
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    st.success(f"Processed {len(upload_file)} files, generated {len(all_chunks)} text chunks.")