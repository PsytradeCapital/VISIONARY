from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[str, List[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected via WebSocket")
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "message": "Connected to Visionary real-time updates",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a WebSocket connection"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
                
            # Clean up empty user entries
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                
        logger.info(f"User {user_id} disconnected from WebSocket")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {str(e)}")
    
    async def send_to_user(self, message: Dict[str, Any], user_id: str):
        """Send a message to all connections for a specific user"""
        if user_id in self.active_connections:
            disconnected_connections = []
            
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {str(e)}")
                    disconnected_connections.append(connection)
            
            # Remove disconnected connections
            for connection in disconnected_connections:
                self.active_connections[user_id].remove(connection)
    
    async def broadcast_to_all(self, message: Dict[str, Any]):
        """Broadcast a message to all connected users"""
        for user_id in list(self.active_connections.keys()):
            await self.send_to_user(message, user_id)
    
    def get_user_connection_count(self, user_id: str) -> int:
        """Get the number of active connections for a user"""
        return len(self.active_connections.get(user_id, []))
    
    def get_total_connections(self) -> int:
        """Get total number of active connections"""
        return sum(len(connections) for connections in self.active_connections.values())

# Global connection manager
connection_manager = ConnectionManager()

class RealtimeUpdateService:
    """Service for sending real-time updates to connected clients"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
    
    async def notify_schedule_update(self, user_id: str, schedule_data: Dict[str, Any]):
        """Notify user of schedule updates"""
        message = {
            "type": "schedule_update",
            "data": schedule_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.connection_manager.send_to_user(message, user_id)
    
    async def notify_progress_update(self, user_id: str, progress_data: Dict[str, Any]):
        """Notify user of progress updates"""
        message = {
            "type": "progress_update", 
            "data": progress_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.connection_manager.send_to_user(message, user_id)
    
    async def notify_reminder(self, user_id: str, reminder_data: Dict[str, Any]):
        """Send reminder notification"""
        message = {
            "type": "reminder",
            "data": reminder_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.connection_manager.send_to_user(message, user_id)
    
    async def notify_achievement(self, user_id: str, achievement_data: Dict[str, Any]):
        """Notify user of new achievement"""
        message = {
            "type": "achievement",
            "data": achievement_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.connection_manager.send_to_user(message, user_id)
    
    async def notify_data_sync(self, user_id: str, sync_status: str):
        """Notify user of data synchronization status"""
        message = {
            "type": "data_sync",
            "data": {
                "status": sync_status,
                "message": f"Data synchronization {sync_status}"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.connection_manager.send_to_user(message, user_id)
    
    async def send_system_notification(self, user_id: str, notification: Dict[str, Any]):
        """Send general system notification"""
        message = {
            "type": "system_notification",
            "data": notification,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.connection_manager.send_to_user(message, user_id)

# Global realtime service
realtime_service = RealtimeUpdateService(connection_manager)