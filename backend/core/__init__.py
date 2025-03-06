"""
Core package for the AI Text Generation API.

This package contains the core functionality of the API:
- Configuration management
- Key management
- Text generation
- Error handling
"""

from core.config import *
from core.exceptions import *
from core.key_manager import key_manager
from core.text_generation import text_generator

__version__ = "1.0.0"