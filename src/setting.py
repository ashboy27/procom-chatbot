import logging
import os
from typing import List, Optional

from dotenv import load_dotenv
from supabase import Client, create_client
from langchain_voyageai import VoyageAIEmbeddings


class Settings:

    def __init__(self, env_file: Optional[str] = None) -> None:
        load_dotenv(env_file)
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        self._supabase: Optional[Client] = None
    

    def get_supabase_client(self) -> Client:
        if self._supabase is None:
            if not self.supabase_url or not self.supabase_key:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
            self._supabase = create_client(self.supabase_url, self.supabase_key)
        return self._supabase
    
    def get_voyage_embedding(self, model_name: str = "voyage-4-large", text: str = "") -> List[float]:
        api_key = os.getenv("VOYAGE_API_KEY")
        if not api_key:
            raise ValueError("VOYAGE_API_KEY not found")
        embedding_model = VoyageAIEmbeddings(api_key=api_key, model=model_name)
        return embedding_model.embed_query(text)



settings = Settings()

def get_logger(name: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)




def get_supabase_client() -> Client:
    return settings.get_supabase_client()

def get_voyage_embedding(text: str, model_name: str = "voyage-4-large") -> List[float]:
    return settings.get_voyage_embedding(model_name=model_name, text=text)