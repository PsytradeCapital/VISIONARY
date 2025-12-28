"""
Secure file storage service with encryption and cloud backup
Task 3.4: Implement cloud-based secure file storage with encryption
"""

import asyncio
import os
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, BinaryIO
from pathlib import Path
import aiofiles
import aiofiles.os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from ..core.config import settings

class FileStorageService:
    """Secure file storage service with encryption and cloud backup"""
    
    def __init__(self):
        # Storage paths
        self.local_storage_path = Path(settings.LOCAL_STORAGE_PATH) if hasattr(settings, 'LOCAL_STORAGE_PATH') else Path("./storage")
        self.encrypted_storage_path = self.local_storage_path / "encrypted"
        self.temp_storage_path = self.local_storage_path / "temp"
        
        # Create directories if they don't exist
        self.local_storage_path.mkdir(parents=True, exist_ok=True)
        self.encrypted_storage_path.mkdir(parents=True, exist_ok=True)
        self.temp_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Encryption settings
        self.encryption_enabled = True
        self.key_rotation_enabled = True
        
        # Cloud storage settings (placeholder for S3/GCS integration)
        self.cloud_backup_enabled = hasattr(settings, 'AWS_S3_BUCKET') or hasattr(settings, 'GCS_BUCKET')
        
    def _generate_encryption_key(self, password: bytes = None) -> bytes:
        """Generate encryption key from password or random"""
        if password is None:
            password = os.urandom(32)
        
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _get_user_encryption_key(self, user_id: int) -> bytes:
        """Get or create user-specific encryption key"""
        key_file = self.encrypted_storage_path / f"user_{user_id}.key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key for user
            key = self._generate_encryption_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    async def store_file(
        self,
        file_content: bytes,
        filename: str,
        user_id: int,
        document_uuid: str,
        encrypted: bool = True,
        cloud_backup: bool = True
    ) -> Dict[str, Any]:
        """
        Store file securely with optional encryption and cloud backup
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            user_id: User ID for access control
            document_uuid: Unique document identifier
            encrypted: Whether to encrypt the file
            cloud_backup: Whether to backup to cloud storage
        """
        try:
            # Generate storage path
            user_dir = self.local_storage_path / f"user_{user_id}"
            user_dir.mkdir(exist_ok=True)
            
            # Generate unique filename
            file_extension = Path(filename).suffix
            storage_filename = f"{document_uuid}{file_extension}"
            storage_path = user_dir / storage_filename
            
            # Encrypt file if requested
            encryption_key_id = None
            if encrypted and self.encryption_enabled:
                encryption_key = self._get_user_encryption_key(user_id)
                fernet = Fernet(encryption_key)
                encrypted_content = fernet.encrypt(file_content)
                file_content_to_store = encrypted_content
                encryption_key_id = f"user_{user_id}_key"
            else:
                file_content_to_store = file_content
            
            # Store file locally
            async with aiofiles.open(storage_path, 'wb') as f:
                await f.write(file_content_to_store)
            
            # Calculate file hash for integrity
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            # Store metadata
            metadata = {
                "original_filename": filename,
                "storage_filename": storage_filename,
                "storage_path": str(storage_path),
                "file_size": len(file_content),
                "encrypted": encrypted,
                "encryption_key_id": encryption_key_id,
                "file_hash": file_hash,
                "stored_at": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "document_uuid": document_uuid
            }
            
            # Save metadata file
            metadata_path = storage_path.with_suffix('.meta')
            async with aiofiles.open(metadata_path, 'w') as f:
                import json
                await f.write(json.dumps(metadata, indent=2))
            
            # Cloud backup if enabled
            cloud_url = None
            if cloud_backup and self.cloud_backup_enabled:
                try:
                    cloud_url = await self._backup_to_cloud(
                        file_content_to_store, storage_filename, user_id, metadata
                    )
                except Exception as e:
                    print(f"Cloud backup failed: {e}")
            
            return {
                "success": True,
                "storage_path": str(storage_path),
                "encryption_key_id": encryption_key_id,
                "file_hash": file_hash,
                "cloud_url": cloud_url,
                "public_url": self._generate_public_url(storage_path) if not encrypted else None,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "storage_path": None
            }
    
    async def retrieve_file(
        self,
        storage_path: str,
        user_id: int,
        encryption_key_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve and decrypt file
        
        Args:
            storage_path: Path to stored file
            user_id: User ID for access control
            encryption_key_id: Encryption key identifier
        """
        try:
            storage_path_obj = Path(storage_path)
            
            # Verify user access
            if f"user_{user_id}" not in str(storage_path_obj):
                raise PermissionError("Access denied to file")
            
            # Check if file exists
            if not storage_path_obj.exists():
                raise FileNotFoundError("File not found")
            
            # Read file content
            async with aiofiles.open(storage_path_obj, 'rb') as f:
                file_content = await f.read()
            
            # Decrypt if encrypted
            if encryption_key_id:
                encryption_key = self._get_user_encryption_key(user_id)
                fernet = Fernet(encryption_key)
                file_content = fernet.decrypt(file_content)
            
            # Read metadata if available
            metadata_path = storage_path_obj.with_suffix('.meta')
            metadata = {}
            if metadata_path.exists():
                async with aiofiles.open(metadata_path, 'r') as f:
                    import json
                    metadata_content = await f.read()
                    metadata = json.loads(metadata_content)
            
            return {
                "success": True,
                "file_content": file_content,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_content": None
            }
    
    async def delete_file(
        self,
        storage_path: str,
        encryption_key_id: Optional[str] = None,
        secure_delete: bool = True
    ) -> Dict[str, Any]:
        """
        Securely delete file and associated data
        
        Args:
            storage_path: Path to stored file
            encryption_key_id: Encryption key identifier
            secure_delete: Whether to perform secure deletion
        """
        try:
            storage_path_obj = Path(storage_path)
            
            # Check if file exists
            if not storage_path_obj.exists():
                return {"success": True, "message": "File already deleted"}
            
            # Secure deletion (overwrite with random data)
            if secure_delete:
                file_size = storage_path_obj.stat().st_size
                
                # Overwrite with random data multiple times
                for _ in range(3):
                    random_data = os.urandom(file_size)
                    async with aiofiles.open(storage_path_obj, 'wb') as f:
                        await f.write(random_data)
            
            # Delete file
            await aiofiles.os.remove(storage_path_obj)
            
            # Delete metadata file
            metadata_path = storage_path_obj.with_suffix('.meta')
            if metadata_path.exists():
                await aiofiles.os.remove(metadata_path)
            
            # Delete from cloud backup if exists
            try:
                await self._delete_from_cloud(storage_path_obj.name)
            except Exception as e:
                print(f"Cloud deletion failed: {e}")
            
            return {
                "success": True,
                "message": "File securely deleted",
                "secure_delete_performed": secure_delete
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _backup_to_cloud(
        self,
        file_content: bytes,
        filename: str,
        user_id: int,
        metadata: Dict[str, Any]
    ) -> Optional[str]:
        """Backup file to cloud storage (S3/GCS)"""
        # Placeholder for cloud backup implementation
        # This would integrate with:
        # - AWS S3 using boto3
        # - Google Cloud Storage using google-cloud-storage
        # - Azure Blob Storage using azure-storage-blob
        
        try:
            # Simulate cloud upload
            await asyncio.sleep(0.1)
            
            # Return mock cloud URL
            cloud_url = f"https://cloud-storage.example.com/user_{user_id}/{filename}"
            return cloud_url
            
        except Exception as e:
            raise Exception(f"Cloud backup failed: {str(e)}")
    
    async def _delete_from_cloud(self, filename: str) -> bool:
        """Delete file from cloud storage"""
        # Placeholder for cloud deletion
        try:
            await asyncio.sleep(0.1)
            return True
        except Exception as e:
            print(f"Cloud deletion error: {e}")
            return False
    
    def _generate_public_url(self, storage_path: Path) -> Optional[str]:
        """Generate public URL for non-encrypted files"""
        if not storage_path.exists():
            return None
        
        # Generate relative URL for serving files
        relative_path = storage_path.relative_to(self.local_storage_path)
        return f"/files/{relative_path}"
    
    async def cleanup_temp_files(self, max_age_hours: int = 24) -> Dict[str, Any]:
        """Clean up temporary files older than specified age"""
        try:
            import time
            
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            deleted_count = 0
            deleted_size = 0
            
            for file_path in self.temp_storage_path.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    
                    if file_age > max_age_seconds:
                        file_size = file_path.stat().st_size
                        await aiofiles.os.remove(file_path)
                        deleted_count += 1
                        deleted_size += file_size
            
            return {
                "success": True,
                "deleted_files": deleted_count,
                "deleted_size_bytes": deleted_size,
                "max_age_hours": max_age_hours
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "deleted_files": 0
            }
    
    async def get_storage_stats(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get storage statistics"""
        try:
            stats = {
                "total_files": 0,
                "total_size_bytes": 0,
                "encrypted_files": 0,
                "unencrypted_files": 0,
                "user_directories": 0
            }
            
            if user_id:
                # Stats for specific user
                user_dir = self.local_storage_path / f"user_{user_id}"
                if user_dir.exists():
                    for file_path in user_dir.iterdir():
                        if file_path.is_file() and not file_path.name.endswith('.meta'):
                            stats["total_files"] += 1
                            stats["total_size_bytes"] += file_path.stat().st_size
                            
                            # Check if encrypted (has corresponding .meta file)
                            metadata_path = file_path.with_suffix('.meta')
                            if metadata_path.exists():
                                async with aiofiles.open(metadata_path, 'r') as f:
                                    import json
                                    metadata = json.loads(await f.read())
                                    if metadata.get("encrypted", False):
                                        stats["encrypted_files"] += 1
                                    else:
                                        stats["unencrypted_files"] += 1
            else:
                # Global stats
                for user_dir in self.local_storage_path.iterdir():
                    if user_dir.is_dir() and user_dir.name.startswith("user_"):
                        stats["user_directories"] += 1
                        
                        for file_path in user_dir.iterdir():
                            if file_path.is_file() and not file_path.name.endswith('.meta'):
                                stats["total_files"] += 1
                                stats["total_size_bytes"] += file_path.stat().st_size
            
            return stats
            
        except Exception as e:
            return {
                "error": str(e),
                "total_files": 0,
                "total_size_bytes": 0
            }