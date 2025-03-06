import pandas as pd
from typing import Dict, List, Optional
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeyRotator:
    def __init__(self):
        self.current_indices: Dict[str, int] = {}
        self.api_keys: Dict[str, List[str]] = {}
        self.models_map: Dict[str, str] = {}
        self._load_api_keys()
        self._load_models()

    def _load_api_keys(self) -> None:
        """Load API keys from CSV file and initialize rotation indices."""
        try:
            keys_df = pd.read_csv('apikeys.csv')
            # Map model provider names to API key provider names
            provider_map = {
                "GROQ MODELS": "GROQ API ",  # Note the trailing space
                "COHERE": "COHERE  AI",
                "SambaNova": "Samba api key",
                "GEMINI": "GEMINI API"
            }
            
            logger.info("Available API key columns: %s", keys_df.columns.tolist())
            
            for model_provider, api_provider in provider_map.items():
                logger.info(f"Processing provider mapping: {model_provider} -> {api_provider}")
                if api_provider in keys_df.columns:
                    valid_keys = [key for key in keys_df[api_provider].dropna()]
                    logger.info(f"Found {len(valid_keys)} valid keys for {model_provider}")
                    if valid_keys:
                        self.api_keys[model_provider] = valid_keys
                        self.current_indices[model_provider] = 0
                else:
                    logger.warning(f"API provider column {api_provider} not found in CSV")
                    logger.warning(f"Available columns: {keys_df.columns.tolist()}")
        except Exception as e:
            logger.error(f"Error loading API keys: {str(e)}")
            raise Exception(f"Error loading API keys: {str(e)}")

    def _load_models(self) -> None:
        """Load models from CSV file and create model-to-provider mapping."""
        try:
            models_df = pd.read_csv('MODELS.csv')
            logger.info("Available model providers: %s", models_df.columns.tolist())
            for column in models_df.columns:
                provider = column.strip()
                models = [model for model in models_df[column].dropna()]
                logger.info(f"Loading {len(models)} models for provider {provider}")
                for model in models:
                    self.models_map[model.strip()] = provider
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise Exception(f"Error loading models: {str(e)}")

    def get_next_key(self, provider: str) -> str:
        """Get the next API key for the specified provider using rotation."""
        if provider not in self.api_keys:
            logger.error(f"No API keys found for provider: {provider}")
            logger.error(f"Available providers: {list(self.api_keys.keys())}")
            raise ValueError(f"No API keys found for provider: {provider}")

        keys = self.api_keys[provider]
        current_idx = self.current_indices[provider]
        total_keys = len(keys)
        
        # Get current key and update index for next time
        key = keys[current_idx]
        next_idx = (current_idx + 1) % total_keys
        self.current_indices[provider] = next_idx
        
        # Log key rotation info with more details
        key_preview = f"{key[:4]}...{key[-4:]}"
        logger.info(f"### API Key Rotation for {provider} ###")
        logger.info(f"Using key #{current_idx + 1}/{total_keys} ({key_preview})")
        logger.info(f"Next request will use key #{next_idx + 1}/{total_keys}")
        logger.info(f"#################################")
        
        return key

    def get_provider_for_model(self, model: str) -> str:
        """Get the provider name for a given model."""
        model = model.strip()
        if model not in self.models_map:
            raise ValueError(f"Model not found: {model}")
        return self.models_map[model]

    def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of all available models with their providers."""
        return [{"model": model, "provider": provider} 
                for model, provider in self.models_map.items()]

# Global instance
key_rotator = KeyRotator()