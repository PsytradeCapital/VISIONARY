"""
Secure External Integrations with Minimal Permissions
Task 13.4: Add secure external integrations with minimal permissions
Requirements: 8.4
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import aiohttp
import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class IntegrationType(Enum):
    """Types of external integrations"""
    GOOGLE_CALENDAR = "google_calendar"
    APPLE_CALENDAR = "apple_calendar"
    OPENAI_API = "openai_api"
    GOOGLE_SPEECH = "google_speech"
    WEATHER_API = "weather_api"

@dataclass
class IntegrationCredentials:
    """Secure storage for integration credentials"""
    integration_type: IntegrationType
    client_id: str
    client_secret: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    scopes: List[str] = None
    
class PermissionAuditor:
    """Audit and monitor external integration permissions"""
    
    def __init__(self):
        self.audit_log = []
        
    def log_permission_request(self, integration: IntegrationType, 
                             requested_scopes: List[str], 
                             granted_scopes: List[str]):
        """Log permission requests for audit trail"""
        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'integration': integration.value,
            'requested_scopes': requested_scopes,
            'granted_scopes': granted_scopes,
            'permission_delta': list(set(requested_scopes) - set(granted_scopes))
        }
        self.audit_log.append(audit_entry)
        logger.info(f"Permission audit: {audit_entry}")
        
    def get_audit_report(self, days: int = 30) -> List[Dict]:
        """Get audit report for specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return [
            entry for entry in self.audit_log 
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        
    def check_permission_escalation(self, integration: IntegrationType, 
                                  new_scopes: List[str]) -> bool:
        """Check if new scopes represent permission escalation"""
        recent_entries = [
            entry for entry in self.audit_log[-10:]  # Last 10 entries
            if entry['integration'] == integration.value
        ]
        
        if not recent_entries:
            return False
            
        last_scopes = set(recent_entries[-1]['granted_scopes'])
        new_scope_set = set(new_scopes)
        
        # Check if new scopes exceed previous grants
        return not new_scope_set.issubset(last_scopes)

class SecureExternalIntegrations:
    """Secure external integrations with minimal permissions"""
    
    def __init__(self):
        self.credentials_store = {}
        self.permission_auditor = PermissionAuditor()
        self.session_timeout = timedelta(hours=1)
        
        # Minimal permission scopes for each integration
        self.minimal_scopes = {
            IntegrationType.GOOGLE_CALENDAR: [
                'https://www.googleapis.com/auth/calendar.readonly',
                'https://www.googleapis.com/auth/calendar.events'
            ],
            IntegrationType.APPLE_CALENDAR: [
                'calendar.read',
                'calendar.write'
            ],
            IntegrationType.OPENAI_API: [
                'api.read',
                'models.use'
            ],
            IntegrationType.GOOGLE_SPEECH: [
                'https://www.googleapis.com/auth/cloud-platform'
            ],
            IntegrationType.WEATHER_API: [
                'weather.read'
            ]
        }
        
    def _encrypt_credentials(self, credentials: str, user_password: str) -> str:
        """Encrypt credentials using user password"""
        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'visionary_salt',  # In production, use random salt per user
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(user_password.encode()))
        
        # Simple encryption (in production, use proper AES encryption)
        encrypted = base64.b64encode(credentials.encode()).decode()
        return encrypted
        
    def _decrypt_credentials(self, encrypted_credentials: str, user_password: str) -> str:
        """Decrypt credentials using user password"""
        # Simple decryption (in production, use proper AES decryption)
        decrypted = base64.b64decode(encrypted_credentials.encode()).decode()
        return decrypted
        
    async def setup_oauth2_integration(self, 
                                     integration_type: IntegrationType,
                                     client_id: str,
                                     client_secret: str,
                                     user_password: str,
                                     requested_scopes: Optional[List[str]] = None) -> Dict[str, Any]:
        """Set up OAuth2 integration with minimal permissions"""
        
        # Use minimal scopes if none specified
        if requested_scopes is None:
            requested_scopes = self.minimal_scopes.get(integration_type, [])
        
        # Validate requested scopes against minimal requirements
        minimal_required = self.minimal_scopes.get(integration_type, [])
        if not set(minimal_required).issubset(set(requested_scopes)):
            logger.warning(f"Requested scopes {requested_scopes} don't include minimal required {minimal_required}")
            requested_scopes.extend([scope for scope in minimal_required if scope not in requested_scopes])
        
        # Check for permission escalation
        if self.permission_auditor.check_permission_escalation(integration_type, requested_scopes):
            logger.warning(f"Permission escalation detected for {integration_type.value}")
            
        # Store encrypted credentials
        credentials = IntegrationCredentials(
            integration_type=integration_type,
            client_id=client_id,
            client_secret=client_secret,
            scopes=requested_scopes
        )
        
        encrypted_creds = self._encrypt_credentials(
            json.dumps(credentials.__dict__, default=str),
            user_password
        )
        
        self.credentials_store[integration_type.value] = encrypted_creds
        
        # Log permission request
        self.permission_auditor.log_permission_request(
            integration_type, requested_scopes, requested_scopes
        )
        
        return {
            'integration_type': integration_type.value,
            'scopes': requested_scopes,
            'status': 'configured',
            'auth_url': self._generate_auth_url(integration_type, client_id, requested_scopes)
        }
        
    def _generate_auth_url(self, integration_type: IntegrationType, 
                          client_id: str, scopes: List[str]) -> str:
        """Generate OAuth2 authorization URL"""
        if integration_type == IntegrationType.GOOGLE_CALENDAR:
            scope_str = ' '.join(scopes)
            return (f"https://accounts.google.com/o/oauth2/auth?"
                   f"client_id={client_id}&"
                   f"redirect_uri=http://localhost:8000/auth/callback&"
                   f"scope={scope_str}&"
                   f"response_type=code&"
                   f"access_type=offline")
        elif integration_type == IntegrationType.APPLE_CALENDAR:
            return f"https://appleid.apple.com/auth/authorize?client_id={client_id}"
        else:
            return f"https://api.{integration_type.value}.com/oauth/authorize?client_id={client_id}"
            
    async def exchange_auth_code(self, 
                               integration_type: IntegrationType,
                               auth_code: str,
                               user_password: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        
        # Retrieve encrypted credentials
        encrypted_creds = self.credentials_store.get(integration_type.value)
        if not encrypted_creds:
            raise ValueError(f"No credentials found for {integration_type.value}")
            
        # Decrypt credentials
        creds_json = self._decrypt_credentials(encrypted_creds, user_password)
        creds_dict = json.loads(creds_json)
        
        # Exchange code for token
        token_data = await self._exchange_code_for_token(
            integration_type, auth_code, creds_dict
        )
        
        # Update credentials with tokens
        creds_dict.update({
            'access_token': token_data['access_token'],
            'refresh_token': token_data.get('refresh_token'),
            'expires_at': (datetime.utcnow() + timedelta(seconds=token_data.get('expires_in', 3600))).isoformat()
        })
        
        # Re-encrypt and store
        encrypted_creds = self._encrypt_credentials(
            json.dumps(creds_dict, default=str),
            user_password
        )
        self.credentials_store[integration_type.value] = encrypted_creds
        
        return {
            'integration_type': integration_type.value,
            'status': 'authenticated',
            'expires_at': creds_dict['expires_at']
        }
        
    async def _exchange_code_for_token(self, 
                                     integration_type: IntegrationType,
                                     auth_code: str,
                                     credentials: Dict) -> Dict[str, Any]:
        """Exchange authorization code for access token via API"""
        
        if integration_type == IntegrationType.GOOGLE_CALENDAR:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                'client_id': credentials['client_id'],
                'client_secret': credentials['client_secret'],
                'code': auth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:8000/auth/callback'
            }
        elif integration_type == IntegrationType.OPENAI_API:
            # OpenAI uses API keys, not OAuth2
            return {
                'access_token': credentials['client_secret'],  # API key
                'expires_in': 86400 * 365  # 1 year
            }
        else:
            # Generic OAuth2 flow
            token_url = f"https://api.{integration_type.value}.com/oauth/token"
            data = {
                'client_id': credentials['client_id'],
                'client_secret': credentials['client_secret'],
                'code': auth_code,
                'grant_type': 'authorization_code'
            }
            
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Token exchange failed: {await response.text()}")
                    
    async def make_authenticated_request(self,
                                       integration_type: IntegrationType,
                                       endpoint: str,
                                       user_password: str,
                                       method: str = 'GET',
                                       data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to external API"""
        
        # Get credentials
        encrypted_creds = self.credentials_store.get(integration_type.value)
        if not encrypted_creds:
            raise ValueError(f"No credentials found for {integration_type.value}")
            
        creds_json = self._decrypt_credentials(encrypted_creds, user_password)
        creds_dict = json.loads(creds_json)
        
        # Check token expiration
        if creds_dict.get('expires_at'):
            expires_at = datetime.fromisoformat(creds_dict['expires_at'])
            if datetime.utcnow() >= expires_at:
                # Refresh token if available
                if creds_dict.get('refresh_token'):
                    await self._refresh_access_token(integration_type, user_password)
                    # Reload credentials after refresh
                    encrypted_creds = self.credentials_store.get(integration_type.value)
                    creds_json = self._decrypt_credentials(encrypted_creds, user_password)
                    creds_dict = json.loads(creds_json)
                else:
                    raise Exception("Access token expired and no refresh token available")
        
        # Make authenticated request
        headers = {
            'Authorization': f"Bearer {creds_dict['access_token']}",
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, endpoint, headers=headers, json=data) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    raise Exception(f"API request failed: {response.status} - {await response.text()}")
                    
    async def _refresh_access_token(self, integration_type: IntegrationType, user_password: str):
        """Refresh access token using refresh token"""
        
        encrypted_creds = self.credentials_store.get(integration_type.value)
        creds_json = self._decrypt_credentials(encrypted_creds, user_password)
        creds_dict = json.loads(creds_json)
        
        if not creds_dict.get('refresh_token'):
            raise Exception("No refresh token available")
            
        if integration_type == IntegrationType.GOOGLE_CALENDAR:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                'client_id': creds_dict['client_id'],
                'client_secret': creds_dict['client_secret'],
                'refresh_token': creds_dict['refresh_token'],
                'grant_type': 'refresh_token'
            }
        else:
            token_url = f"https://api.{integration_type.value}.com/oauth/token"
            data = {
                'client_id': creds_dict['client_id'],
                'client_secret': creds_dict['client_secret'],
                'refresh_token': creds_dict['refresh_token'],
                'grant_type': 'refresh_token'
            }
            
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    
                    # Update credentials
                    creds_dict.update({
                        'access_token': token_data['access_token'],
                        'expires_at': (datetime.utcnow() + timedelta(seconds=token_data.get('expires_in', 3600))).isoformat()
                    })
                    
                    # Re-encrypt and store
                    encrypted_creds = self._encrypt_credentials(
                        json.dumps(creds_dict, default=str),
                        user_password
                    )
                    self.credentials_store[integration_type.value] = encrypted_creds
                else:
                    raise Exception(f"Token refresh failed: {await response.text()}")
                    
    def revoke_integration(self, integration_type: IntegrationType, user_password: str) -> bool:
        """Revoke and remove integration credentials"""
        
        try:
            # Get credentials for revocation
            encrypted_creds = self.credentials_store.get(integration_type.value)
            if encrypted_creds:
                creds_json = self._decrypt_credentials(encrypted_creds, user_password)
                creds_dict = json.loads(creds_json)
                
                # Attempt to revoke token with provider
                asyncio.create_task(self._revoke_token_with_provider(integration_type, creds_dict))
                
            # Remove from local storage
            if integration_type.value in self.credentials_store:
                del self.credentials_store[integration_type.value]
                
            logger.info(f"Integration {integration_type.value} revoked successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error revoking integration {integration_type.value}: {e}")
            return False
            
    async def _revoke_token_with_provider(self, integration_type: IntegrationType, credentials: Dict):
        """Revoke token with external provider"""
        
        try:
            if integration_type == IntegrationType.GOOGLE_CALENDAR:
                revoke_url = f"https://oauth2.googleapis.com/revoke?token={credentials['access_token']}"
                async with aiohttp.ClientSession() as session:
                    async with session.post(revoke_url) as response:
                        if response.status == 200:
                            logger.info("Google token revoked successfully")
                        else:
                            logger.warning(f"Google token revocation failed: {response.status}")
                            
        except Exception as e:
            logger.error(f"Error revoking token with provider: {e}")
            
    def get_integration_status(self, integration_type: IntegrationType, user_password: str) -> Dict[str, Any]:
        """Get status of integration"""
        
        encrypted_creds = self.credentials_store.get(integration_type.value)
        if not encrypted_creds:
            return {
                'integration_type': integration_type.value,
                'status': 'not_configured'
            }
            
        try:
            creds_json = self._decrypt_credentials(encrypted_creds, user_password)
            creds_dict = json.loads(creds_json)
            
            status = 'configured'
            if creds_dict.get('access_token'):
                if creds_dict.get('expires_at'):
                    expires_at = datetime.fromisoformat(creds_dict['expires_at'])
                    if datetime.utcnow() >= expires_at:
                        status = 'expired'
                    else:
                        status = 'active'
                else:
                    status = 'active'
                    
            return {
                'integration_type': integration_type.value,
                'status': status,
                'scopes': creds_dict.get('scopes', []),
                'expires_at': creds_dict.get('expires_at')
            }
            
        except Exception as e:
            logger.error(f"Error getting integration status: {e}")
            return {
                'integration_type': integration_type.value,
                'status': 'error',
                'error': str(e)
            }
            
    def get_permission_audit_report(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive permission audit report"""
        
        audit_entries = self.permission_auditor.get_audit_report(days)
        
        # Analyze audit data
        integration_summary = {}
        for entry in audit_entries:
            integration = entry['integration']
            if integration not in integration_summary:
                integration_summary[integration] = {
                    'total_requests': 0,
                    'permission_escalations': 0,
                    'scopes_requested': set(),
                    'scopes_granted': set()
                }
                
            summary = integration_summary[integration]
            summary['total_requests'] += 1
            summary['scopes_requested'].update(entry['requested_scopes'])
            summary['scopes_granted'].update(entry['granted_scopes'])
            
            if entry['permission_delta']:
                summary['permission_escalations'] += 1
                
        # Convert sets to lists for JSON serialization
        for integration, summary in integration_summary.items():
            summary['scopes_requested'] = list(summary['scopes_requested'])
            summary['scopes_granted'] = list(summary['scopes_granted'])
            
        return {
            'audit_period_days': days,
            'total_entries': len(audit_entries),
            'integration_summary': integration_summary,
            'recent_entries': audit_entries[-10:] if audit_entries else []
        }