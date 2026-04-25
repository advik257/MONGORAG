from exceptions import *
# AWS
import boto3
logger = boto3.client("logs")

# # main.py
# from logger import setup_logging
# setup_logging()          # ✅ call ONCE at startup

# # pdf_processor.py
# from logger import get_logger
# logger = get_logger(__name__)    # → rag_app.pdf_processor
# logger.info("Loading PDF...")

# # embeddings.py
# from logger import get_logger
# logger = get_logger(__name__)    # → rag_app.embeddings
# logger.info("Generating embeddings...")

# # mongo.py
# from logger import get_logger
# logger = get_logger(__name__)    # → rag_app.mongo
# logger.error("Insert failed!")

def main():
    print("Hello from ragmongodb!")


if __name__ == "__main__":
    main()
