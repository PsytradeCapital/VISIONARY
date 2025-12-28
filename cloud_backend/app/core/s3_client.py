"""
AWS S3 client for encrypted file storage
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, BinaryIO
import logging
from cryptography.fernet import Fernet
import base64
import os

from .config import settings

logger = logging.getLogger(__name__)

class S3Service:
    """Encrypted S3 file storage service"""
    
    def __init__(self):
        self.s3_client = None
        self.encryption_key = None
        self._init_s3_client()
        self._init_encryption()
    
    def _init_s3_client(self):
        """Initialize S3 client"""
        try:
            if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION
                )
            else:
                # Use IAM role or environment credentials
                self.s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
            
            logger.info("S3 client initialized")
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except Exception as e:
            logger.error(f"S3 client initialization failed: {e}")
            raise
    
    def _init_encryption(self):
        """Initialize encryption key"""
        try:
            # Use provided key or generate new one
            if settings.ENCRYPTION_KEY:
                key = settings.ENCRYPTION_KEY.encode()
                # Ensure key is 32 bytes for Fernet
                key = base64.urlsafe_b64encode(key[:32].ljust(32, b'0'))
            else:
                key = Fernet.generate_key()
            
            self.encryption_key = Fernet(key)
            logger.info("Encryption initialized")
        except Exception as e:
            logger.error(f"Encryption initialization failed: {e}")
            raise
    
    def _encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data before storage"""
        return self.encryption_key.encrypt(data)
    
    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt data after retrieval"""
        return self.encryption_key.decrypt(encrypted_data)
    
    async def upload_file(self, file_data: bytes, key: str, content_type: str = "application/octet-stream") -> bool:
        """Upload encrypted file to S3"""
        try:
            # Encrypt file data
            encrypted_data = self._encrypt_data(file_data)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=key,
                Body=encrypted_data,
                ContentType=content_type,
                ServerSideEncryption='AES256'  # Additional S3 encryption
            )
            
            logger.info(f"File uploaded successfully: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            return False
        except Exception as e:
            logger.error(f"File upload error: {e}")
            return False
    
    async def download_file(self, key: str) -> Optional[bytes]:
        """Download and decrypt file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=key
            )
            
            encrypted_data = response['Body'].read()
            decrypted_data = self._decrypt_data(encrypted_data)
            
            logger.info(f"File downloaded successfully: {key}")
            return decrypted_data
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.warning(f"File not found: {key}")
            else:
                logger.error(f"S3 download failed: {e}")
            return None
        except Exception as e:
            logger.error(f"File download error: {e}")
            return None
    
    async def delete_file(self, key: str) -> bool:
        """Securely delete file from S3"""
        try:
            self.s3_client.delete_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=key
            )
            
            logger.info(f"File deleted successfully: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"S3 delete failed: {e}")
            return False
        except Exception as e:
            logger.error(f"File delete error: {e}")
            return False
    
    async def file_exists(self, key: str) -> bool:
        """Check if file exists in S3"""
        try:
            self.s3_client.head_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=key
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            logger.error(f"S3 head object failed: {e}")
            return False
        except Exception as e:
            logger.error(f"File exists check error: {e}")
            return False

s3_service = S3Service()