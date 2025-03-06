from typing import Dict

# API Provider mapping
PROVIDER_MAP: Dict[str, str] = {
    "GROQ MODELS": "GROQ API ",  # Note the trailing space
    "COHERE": "COHERE  AI",
    "SambaNova": "Samba api key",
    "GEMINI": "GEMINI API"
}

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# CORS Configuration
CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

# Logging Configuration
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        }
    }
}