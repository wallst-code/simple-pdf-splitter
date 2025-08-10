"""Enterprise-grade logging service for Simple PDF Splitter."""

import os
import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from datetime import datetime


class LoggingService:
    """Centralized logging service following enterprise patterns."""
    
    _logger: Optional[logging.Logger] = None
    _initialized: bool = False
    
    @classmethod
    def get_logger(cls, name: str = 'pdf_splitter') -> logging.Logger:
        """Get or create logger instance.
        
        Args:
            name: Logger name (defaults to 'pdf_splitter')
            
        Returns:
            Configured logger instance
        """
        if not cls._initialized:
            cls._setup_logging()
            cls._initialized = True
            
        return logging.getLogger(name)
    
    @classmethod
    def _setup_logging(cls) -> None:
        """Configure logging system."""
        # Get configuration from environment
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        log_file = os.getenv('LOG_FILE', 'logs/app.log')
        max_bytes = int(os.getenv('LOG_MAX_BYTES', '10485760'))  # 10MB
        backup_count = int(os.getenv('LOG_BACKUP_COUNT', '5'))
        
        # Create logs directory if needed
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level))
        
        # Remove existing handlers
        root_logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(getattr(logging, log_level))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # Log initialization
        logger = logging.getLogger('pdf_splitter')
        logger.info(f"Logging initialized - Level: {log_level}, File: {log_file}")
    
    @classmethod
    def log_security_event(cls, event_type: str, details: str, 
                          severity: str = 'WARNING') -> None:
        """Log security-related events.
        
        Args:
            event_type: Type of security event
            details: Event details
            severity: Log level (INFO, WARNING, ERROR, CRITICAL)
        """
        logger = cls.get_logger('security')
        log_method = getattr(logger, severity.lower())
        log_method(f"SECURITY [{event_type}]: {details}")
    
    @classmethod
    def log_error_safe(cls, error: Exception, context: str = '') -> str:
        """Log error details internally, return safe message for user.
        
        Args:
            error: Exception to log
            context: Additional context
            
        Returns:
            Generic error message safe for user display
        """
        logger = cls.get_logger()
        logger.error(f"{context}: {str(error)}", exc_info=True)
        
        # Return generic message for user
        return "An error occurred processing your request. Please try again."
    
    @classmethod
    def log_performance(cls, operation: str, duration: float) -> None:
        """Log performance metrics.
        
        Args:
            operation: Operation name
            duration: Duration in seconds
        """
        logger = cls.get_logger('performance')
        logger.info(f"PERFORMANCE: {operation} completed in {duration:.3f}s")