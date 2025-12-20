from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from websocket_service import connection_manager, realtime_service
from auth import verify_token
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, token: str = Query(...)):
    """WebSocket endpoint for real-time updates"""
    try:
        # Verify the token
        user_data = await verify_token(token)
        
        # Ensure the user_id matches the token
        if user_data["id"] != user_id:
            await websocket.close(code=1008, reason="Unauthorized")
            return
        
        # Accept the connection
        await connection_manager.connect(websocket, user_id)
        
        try:
            while True:
                # Listen for messages from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await connection_manager.send_personal_message({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    }, websocket)
                
                elif message.get("type") == "request_update":
                    # Client requesting specific updates
                    update_type = message.get("update_type")
                    if update_type == "schedule":
                        # Send current schedule data
                        await realtime_service.notify_schedule_update(user_id, {
                            "message": "Schedule data requested",
                            "refresh": True
                        })
                    elif update_type == "progress":
                        # Send current progress data
                        await realtime_service.notify_progress_update(user_id, {
                            "message": "Progress data requested", 
                            "refresh": True
                        })
                
        except WebSocketDisconnect:
            connection_manager.disconnect(websocket, user_id)
            
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {str(e)}")
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass

@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "total_connections": connection_manager.get_total_connections(),
        "active_users": len(connection_manager.active_connections)
    }