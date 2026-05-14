import os
from src.setting import get_logger, get_voyage_embedding
from src.vector_store import VectorStore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


logger = get_logger(__name__)


def load_documents(path: str):
    """Load markdown documents from a directory."""
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
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=1000,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def ingest_documents(path: str = "knowledge") -> bool:
    """Ingest documents into the knowledge base."""
    try:
        documents = load_documents(path)
        if not documents:
            logger.warning(f"No documents found in {path}")
            return False

        logger.info(f"Loaded {len(documents)} documents.")
        chunks = split_text(documents)
        logger.info(f"Split into {len(chunks)} chunks.")
        chunk_data = [
            {
                "content": chunk.page_content,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ]

        logger.info("Generating embeddings...")
        embeddings = []
        for i, chunk_dict in enumerate(chunk_data):
            if i % 10 == 0:
                logger.info(f"Embedding chunk {i}/{len(chunk_data)}")
            embedding = get_voyage_embedding(chunk_dict["content"])
            embeddings.append(embedding)
        logger.info("Storing chunks in local vector store...")
        store = VectorStore("knowledge_base.db")
        store.add_chunks(chunk_data, embeddings)

        if os.getenv("SUPABASE_URL"):
            try:
                from src.setting import get_supabase_client
                logger.info("Also uploading to Supabase...")
                supabase = get_supabase_client()
                for chunk_dict in chunk_data:
                    embedding = get_voyage_embedding(chunk_dict["content"])
                    data = {
                        "content": chunk_dict["content"],
                        "metadata": chunk_dict["metadata"],
                        "embedding": embedding,
                    }
                    supabase.table("knowledge_chunks").insert(data).execute()
                logger.info("Supabase upload complete.")
            except Exception as e:
                logger.warning(f"Supabase upload failed: {e}. Continuing with local store.")

        logger.info("Knowledge base ingestion complete!")
        return True

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return False


if __name__ == "__main__":
    ingest_documents("knowledge")


