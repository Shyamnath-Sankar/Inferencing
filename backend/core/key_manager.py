import pandas as pd
from typing import Dict, List
import logging
import os
from core.config import PROVIDER_MAP
from core.exceptions import APIKeyError

logger = logging.getLogger(__name__)

class KeyManager:
    def __init__(self):
        self.current_indices: Dict[str, int] = {}
        self.api_keys: Dict[str, List[str]] = {}
        self.models_map: Dict[str, str] = {}
        self.provider_map = PROVIDER_MAP.copy()
        self._load_models()  # Load models first to detect providers
        self._load_api_keys()

    def _detect_api_key_column(self, provider: str, columns: List[str]) -> str:
        """
        Detect the API key column name for a provider.
        Tries different common formats like '{PROVIDER} API' or '{PROVIDER} api key'.
        """
        provider_variants = [
            f"{provider} API",
            f"{provider} api",
            f"{provider} API KEY",
            f"{provider} api key",
            provider.upper() + " API",
            provider.lower() + " api",
        ]
        
        for variant in provider_variants:
            for column in columns:
                if column.strip().lower() == variant.lower():
                    return column
        
        return None

    def _load_api_keys(self) -> None:
        """Load API keys from CSV file and initialize rotation indices."""
        try:
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            keys_path = os.path.join(backend_dir, 'apikeys.csv')
            keys_df = pd.read_csv(keys_path)
            
            logger.info("Available API key columns: %s", keys_df.columns.tolist())
            
            # Process both predefined and auto-detected providers
            for provider in set(self.models_map.values()):
                if provider not in self.provider_map:
                    # Try to detect API key column for new provider
                    api_column = self._detect_api_key_column(provider, keys_df.columns)
                    if api_column:
                        self.provider_map[provider] = api_column
                        logger.info(f"Auto-detected API column '{api_column}' for provider '{provider}'")
                
                api_provider = self.provider_map.get(provider)
                if api_provider and api_provider in keys_df.columns:
                    valid_keys = [key for key in keys_df[api_provider].dropna()]
                    logger.info(f"Found {len(valid_keys)} valid keys for {provider}")
                    if valid_keys:
                        self.api_keys[provider] = valid_keys
                        self.current_indices[provider] = 0
                else:
                    logger.warning(f"No API keys found for provider: {provider}")
                    if api_provider:
                        logger.warning(f"Column '{api_provider}' not found in CSV")
                    logger.warning(f"Available columns: {keys_df.columns.tolist()}")
                    
        except Exception as e:
            logger.error(f"Error loading API keys: {str(e)}")
            raise APIKeyError(f"Error loading API keys: {str(e)}")

    def _load_models(self) -> None:
        """Load models from CSV file and create model-to-provider mapping."""
        try:
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            models_path = os.path.join(backend_dir, 'MODELS.csv')
            models_df = pd.read_csv(models_path)
            
            logger.info("Available model providers: %s", models_df.columns.tolist())
            for column in models_df.columns:
                provider = column.strip()
                models = [model for model in models_df[column].dropna()]
                logger.info(f"Loading {len(models)} models for provider {provider}")
                for model in models:
                    self.models_map[model.strip()] = provider
                    
            logger.info(f"Detected providers: {set(self.models_map.values())}")
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise APIKeyError(f"Error loading models: {str(e)}")

    def get_next_key(self, provider: str) -> str:
        """Get the next API key for the specified provider using rotation."""
        if provider not in self.api_keys:
            logger.error(f"No API keys found for provider: {provider}")
            logger.error(f"Available providers: {list(self.api_keys.keys())}")
            raise APIKeyError(f"No API keys found for provider: {provider}")

        keys = self.api_keys[provider]
        current_idx = self.current_indices[provider]
        total_keys = len(keys)
        
        key = keys[current_idx]
        next_idx = (current_idx + 1) % total_keys
        self.current_indices[provider] = next_idx
        
        key_preview = f"{key[:4]}...{key[-4:]}"
        logger.info(f"### API Key Rotation for {provider} ###")
        logger.info(f"Using key #{current_idx + 1}/{total_keys} ({key_preview})")
        logger.info(f"Next request will use key #{next_idx + 1}/{total_keys}")
        
        return key

    def get_provider_for_model(self, model: str) -> str:
        """Get the provider name for a given model."""
        model = model.strip()
        if model not in self.models_map:
            raise APIKeyError(f"Model not found: {model}")
        return self.models_map[model]

    def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of all available models with their providers."""
        return [{"model": model, "provider": provider} 
                for model, provider in self.models_map.items()]

# Global instance
key_manager = KeyManager()