import chromadb
from chromadb.utils import embedding_functions

#setting up Chroma DB
client = chromadb.Client()
collection = client.get_or_create_collection(name = "documents")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def add_chunks_to_vectorstore(chunks):
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"doc_id": chunk["doc_id"], "page": chunk["page"]} for chunk in chunks]
    ids = [chunk["doc_id"] + "-" + str(i) for i in range(len(chunks))]

    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Added {len(documents)} chunks to ChromaDB.")