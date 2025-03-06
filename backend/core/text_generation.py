from typing import AsyncGenerator, Dict, Any
import importlib
import logging
from core.exceptions import ModelError, ProviderError
from core.key_manager import key_manager

logger = logging.getLogger(__name__)

class TextGenerator:
    """Handles text generation across different model providers."""
    
    @staticmethod
    async def generate_stream(model: str, prompt: str) -> AsyncGenerator[str, None]:
        """
        Generate streaming text responses using the specified model.
        
        Args:
            model (str): The name of the model to use
            prompt (str): The input prompt for text generation
            
        Yields:
            str: Generated text chunks
            
        Raises:
            ModelError: If the model is not found or invalid
            ProviderError: If there's an error with the provider
        """
        try:
            # Get provider for the selected model
            provider = key_manager.get_provider_for_model(model)
            logger.info(f"Using provider {provider} for model {model}")
            
            # Get API key
            api_key = key_manager.get_next_key(provider)
            logger.info(f"Retrieved API key for provider {provider}")
            
            # Import provider module
            try:
                module_name = provider.lower().split()[0]  # Get first word in lowercase
                logger.info(f"Importing module: models.{module_name}")
                provider_module = importlib.import_module(f"models.{module_name}")
            except ImportError as e:
                raise ProviderError(f"Provider module not found: {str(e)}")
            
            # Generate text stream
            async for chunk in provider_module.run_model_stream(api_key, model, prompt):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error in generate_stream: {str(e)}")
            raise

    @staticmethod
    def get_available_models() -> Dict[str, Any]:
        """
        Get all available models and their providers.
        
        Returns:
            Dict[str, Any]: Dictionary containing model information
        """
        try:
            models = key_manager.get_available_models()
            return {
                "models": models,
                "total": len(models)
            }
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            raise ModelError(f"Failed to get available models: {str(e)}")

# Global instance
text_generator = TextGenerator()