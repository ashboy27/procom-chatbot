import logging
import os
from typing import Iterable, List, Optional, Sequence, Tuple, Union
from dotenv import load_dotenv
from supabase import Client, create_client


class Settings:

    def __init__(self, env_file: Optional[str] = None) -> None:
        load_dotenv(env_file)
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        self._supabase: Optional[Client] = None
        self._default_headers: List[Tuple[str, str]] = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ]

    def get_supabase_client(self) -> Client:

        if self._supabase is None:
            if not self.supabase_url or not self.supabase_key:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
            self._supabase = create_client(self.supabase_url, self.supabase_key)
        return self._supabase


settings = Settings()


import logging

def get_logger(name: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)




def get_supabase_client() -> Client:
    return settings.get_supabase_client()
