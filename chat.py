from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
from assistant.ai_assistant import AIAssistant

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()
assistant = AIAssistant(provider="gemini")  # You can change the provider here

async def handle_chat(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Get response from AI assistant
            response = await assistant.chat(message_data.get("messages", []))
            
            # Send response back to client
            await manager.send_message(
                json.dumps({"response": response}),
                client_id
            )
    except WebSocketDisconnect:
        manager.disconnect(client_id) 