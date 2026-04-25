import os
from dotenv import load_dotenv

load_dotenv()

# ─── App ──────────────────────────────────────────────────────────────────────
class AppConfig:
    ENV       = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    IS_PROD   = ENV == "production"

# ─── MongoDB ──────────────────────────────────────────────────────────────────
class MongoConfig:
    URI             = os.getenv("MONGODB_URI")
    DB_NAME         = os.getenv("MONGODB_DB_NAME",         "Invoice_database")
    COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "inoice_pdf_embeddings")
    VECTOR_INDEX    = os.getenv("MONGODB_VECTOR_INDEX",    "vector_index")

# ─── Embedding Model ──────────────────────────────────────────────────────────
class EmbeddingConfig:
    
    PROVIDER      = os.getenv("EMBEDDING_PROVIDER", "cohere")

    # Cohere
    COHERE_API_KEY    = os.getenv("COHERE_API_KEY")
    COHERE_MODEL_DEV  = "embed-english-light-v3.0"   # 384 dims  - dev
    COHERE_MODEL_PROD = "embed-english-v3.0"          # 1024 dims - prod
    COHERE_MODEL      = COHERE_MODEL_PROD if AppConfig.IS_PROD else COHERE_MODEL_DEV
    COHERE_DIMENSIONS = 1024 if AppConfig.IS_PROD else 384

    # OpenAI
    OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # 1536 dims
    OPENAI_DIMENSIONS      = 1536

    # Batch size for embedding API calls
    BATCH_SIZE = 50

# ─── LLM Model ────────────────────────────────────────────────────────────────
class LLMConfig:
    PROVIDER = os.getenv("LLM_PROVIDER", "groq")

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL   = "llama3-8b-8192"
    GROQ_TEMPERATURE = 0.7
    GROQ_MAX_TOKENS  = 1024

    # OpenAI
    OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL     = "gpt-4o-mini"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS  = 1024

# ─── PDF / Document Processing ────────────────────────────────────────────────
class DocumentConfig:
    DATA_DIR      = os.getenv("DATA_DIR", "data/")
    CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE",   "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# ─── Vector Search ────────────────────────────────────────────────────────────
class SearchConfig:
    NUM_CANDIDATES = 500 if AppConfig.IS_PROD else 100
    TOP_K          = int(os.getenv("TOP_K", "5"))
    SIMILARITY     = "cosine"   # cosine | euclidean | dotProduct

# ─── Centralized Settings ─────────────────────────────────────────────────────
class Settings:
    app       = AppConfig()
    mongo     = MongoConfig()
    embedding = EmbeddingConfig()
    llm       = LLMConfig()
    document  = DocumentConfig()
    search    = SearchConfig()

settings = Settings()