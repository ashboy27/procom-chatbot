import os
from langchain_voyageai import VoyageAIEmbeddings
from setting import get_supabase_client, get_logger
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = get_logger(__name__)
embedding_voyage = VoyageAIEmbeddings(api_key=os.getenv("VOYAGE_API_KEY"), model="voyage-4-large")

def embed_text(text):
    """Return embedding vector for a string"""
    return embedding_voyage.embed_query(text) 

from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_documents(path: str):
    logger.info(f"Loading documents from {path}...")

    loader = DirectoryLoader(
        path,
        glob="*.md",
        loader_cls=TextLoader,
        recursive=False
    )

    documents = loader.load()
    logger.info(f"{len(documents)} documents loaded from {path}")
    return documents

def split_text(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def ingest_documents_to_supabase():
    
    path = "test_knowledge"
    documents = load_documents(path)
    logger.info(f"Loaded {len(documents)} documents.")
    chunks = split_text(documents)
    logger.info(f"Split into {len(chunks)} chunks.")
    supabase = get_supabase_client()

    for i, chunk in enumerate(chunks):
        embedding_vector = embed_text(chunk.page_content)
        data = {
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "embedding": embedding_vector,
        }
        supabase.table("knowledge_chunks").insert(data).execute()


def main():
    ingest_documents_to_supabase()
 



main()