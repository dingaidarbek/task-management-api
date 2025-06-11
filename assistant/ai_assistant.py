import os
from typing import Optional
import google.generativeai as genai
from openai import OpenAI
import anthropic

class AIAssistant:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self._setup_provider()

    def _setup_provider(self):
        if self.provider == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel('gemini-pro')
        elif self.provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.provider == "claude":
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def get_response(self, prompt: str) -> str:
        try:
            if self.provider == "gemini":
                response = await self.model.generate_content(prompt)
                return response.text
            elif self.provider == "openai":
                response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            elif self.provider == "claude":
                response = await self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
        except Exception as e:
            return f"Error getting response: {str(e)}"

    async def chat(self, messages: list) -> str:
        try:
            if self.provider == "gemini":
                chat = self.model.start_chat(history=[])
                response = await chat.send_message(messages[-1]["content"])
                return response.text
            elif self.provider == "openai":
                response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                return response.choices[0].message.content
            elif self.provider == "claude":
                response = await self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1000,
                    messages=messages
                )
                return response.content[0].text
        except Exception as e:
            return f"Error in chat: {str(e)}" 