from setting import get_supabase_client, get_logger, get_voyage_embedding
from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


logger = get_logger(__name__)

def load_documents(path: str):

    logger.info(f"Loading documents from {path}...")
    loader = DirectoryLoader(
        path,
        glob="**/*.md",
        loader_cls=TextLoader,
        recursive=True
    )

    documents = loader.load()
    logger.info(f"{len(documents)} documents loaded from {path}")
    return documents

def split_text(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=1000,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def ingest_documents_to_supabase(path: str):
    
    documents = load_documents(path)
    logger.info(f"Loaded {len(documents)} documents.")
    chunks = split_text(documents)
    logger.info(f"Split into {len(chunks)} chunks.")
    supabase = get_supabase_client()

    for i, chunk in enumerate(chunks):
        embedding_vector = get_voyage_embedding(chunk.page_content)
        data = {
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "embedding": embedding_vector,
        }
        supabase.table("knowledge_chunks").insert(data).execute()

ingest_documents_to_supabase("knowledge")
 

