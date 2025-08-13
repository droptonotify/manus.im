from typing import List, Dict, Any, Optional
import httpx
from app.domain.external.llm import LLM
from app.core.config import get_settings
import logging
import json

logger = logging.getLogger(__name__)

class GoogleGenAILLM(LLM):
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.api_key
        self.api_base = settings.api_base
        self._model_name = settings.model_name
        self._temperature = settings.temperature
        self._max_tokens = settings.max_tokens
        self.client = httpx.AsyncClient()
        logger.info(f"Initialized Google Generative AI LLM with model: {self._model_name}")

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    async def ask(self, messages: List[Dict[str, str]],
                tools: Optional[List[Dict[str, Any]]] = None,
                response_format: Optional[Dict[str, Any]] = None,
                tool_choice: Optional[str] = None) -> Dict[str, Any]:
        """Send chat request to Google Generative AI API"""
        url = f"{self.api_base}/{self._model_name}:generateContent?key={self.api_key}"
        
        # Convert messages to Google's format
        contents = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            if role and content:
                # Convert role 'assistant' to 'model'
                if role == "assistant":
                    role = "model"
                contents.append({"role": role, "parts": [{"text": content}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": self._temperature,
                "maxOutputTokens": self._max_tokens,
            }
        }
        
        if tools:
            # Convert tools to Google's format if necessary
            # This is a placeholder for actual tool conversion logic
            payload["tools"] = tools

        headers = {"Content-Type": "application/json"}

        try:
            response = await self.client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            
            # Transform Google's response back to OpenAI's format
            text_content = response_data['candidates'][0]['content']['parts'][0]['text']
            
            return {
                "content": text_content,
                "tool_calls": None, # Placeholder for tool call handling
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"Error calling Google GenAI API: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Error code: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error calling Google GenAI API: {str(e)}")
            raise
