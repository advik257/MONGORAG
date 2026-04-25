"""
Centralized logging configuration for RAG MongoDB application.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    is_lambda = os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None

    # ✅ consistent name across app
    
    logger = logging.getLogger("rag_app")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    if is_lambda:
        # Lambda — stdout only (CloudWatch captures this)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(handler)

    else:
        # Local — console + file handlers
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # ── Formatters ────────────────────────────────────────────────────────
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # ── Console Handler ───────────────────────────────────────────────────
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        # ── File Handler (all logs) ───────────────────────────────────────────
        file_handler = RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=10_000_000,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        # ── Error Handler (errors only) ───────────────────────────────────────
        error_handler = RotatingFileHandler(
            log_dir / "error.log",
            maxBytes=5_000_000,   # 5MB
            backupCount=3,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a child logger for a specific module.
    Inherits handlers from parent 'rag_app' logger.

    Usage:
        logger = get_logger(__name__)
    """
    return logging.getLogger(f"rag_app.{name}")  # ✅ child logger


if __name__ == "__main__":
    setup_logging("DEBUG")
    logger = get_logger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")