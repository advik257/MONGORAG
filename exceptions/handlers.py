import logging
import traceback
from functools import wraps

logger = logging.getLogger(__name__)

# ─── Base Exception ───────────────────────────────────────────────────────────

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message     = message
        self.status_code = status_code
        self.details     = details or {}
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.status_code}] {self.message} | Details: {self.details}"

# ─── MongoDB Exceptions ───────────────────────────────────────────────────────

class MongoConnectionError(AppException):
    def __init__(self, details: dict = None):
        super().__init__(
            message     = "Failed to connect to MongoDB",
            status_code = 503,
            details     = details
        )

class MongoInsertError(AppException):
    def __init__(self, details: dict = None):
        super().__init__(
            message     = "Failed to insert document into MongoDB",
            status_code = 500,
            details     = details
        )

class MongoSearchError(AppException):
    def __init__(self, details: dict = None):
        super().__init__(
            message     = "Failed to perform vector search in MongoDB",
            status_code = 500,
            details     = details
        )

# ─── Embedding Exceptions ─────────────────────────────────────────────────────

class EmbeddingError(AppException):
    def __init__(self, details: dict = None):
        super().__init__(
            message     = "Failed to generate embeddings",
            status_code = 500,
            details     = details
        )

class EmbeddingBatchError(AppException):
    def __init__(self, batch_index: int, details: dict = None):
        super().__init__(
            message     = f"Failed to embed batch at index {batch_index}",
            status_code = 500,
            details     = details
        )

# ─── PDF Exceptions ───────────────────────────────────────────────────────────

class PDFLoadError(AppException):
    def __init__(self, filename: str, details: dict = None):
        super().__init__(
            message     = f"Failed to load PDF: {filename}",
            status_code = 400,
            details     = details
        )

class PDFChunkError(AppException):
    def __init__(self, details: dict = None):
        super().__init__(
            message     = "Failed to split PDF into chunks",
            status_code = 500,
            details     = details
        )

# ─── LLM Exceptions ───────────────────────────────────────────────────────────

class LLMError(AppException):
    def __init__(self, details: dict = None):
        super().__init__(
            message     = "Failed to get response from LLM",
            status_code = 500,
            details     = details
        )

# ─── Config Exceptions ────────────────────────────────────────────────────────

class ConfigError(AppException):
    def __init__(self, key: str, details: dict = None):
        super().__init__(
            message     = f"Missing or invalid config key: {key}",
            status_code = 500,
            details     = details
        )

# ─── Global Exception Handler Decorator ──────────────────────────────────────

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppException as e:
            logger.error(f"AppException in '{func.__name__}': {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error in '{func.__name__}': {str(e)}\n"
                f"{traceback.format_exc()}"
            )
            raise AppException(
                message     = f"Unexpected error in {func.__name__}",
                status_code = 500,
                details     = {"error": str(e), "trace": traceback.format_exc()}
            )
    return wrapper