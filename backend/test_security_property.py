"""
Property Test for Comprehensive Data Security
Task 13.3: Write property test for comprehensive data security
Requirements: 1.4, 8.1, 8.2, 8.3, 8.4, 8.5

Feature: ai-personal-scheduler
Property 3: Comprehensive data security
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, invariant
import tempfile
import os
import json
from datetime import datetime, timedelta
from security_service import SecurityService, SecurityException
from cleanup_service import CleanupService

# Test data generators
@st.composite
def user_data(draw):
    """Generate realistic user data for testing"""
    return {
        'user_id': draw(st.text(min_size=8, max_size=32, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        'email': draw(st.emails()),
        'password': draw(st.text(min_size=8, max_size=128)),
        'personal_info': {
            'name': draw(st.text(min_size=1, max_size=100)),
            'phone': draw(st.text(min_size=10, max_size=15, alphabet='0123456789')),
            'address': draw(st.text(min_size=10, max_size=200))
        },
        'sensitive_data': {
            'ssn': draw(st.text(min_size=9, max_size=11, alphabet='0123456789')),
            'credit_card': draw(st.text(min_size=13, max_size=19, alphabet='0123456789')),
            'medical_info': draw(st.text(min_size=10, max_size=500))
        },
        'preferences': {
            'theme': draw(st.sampled_from(['light', 'dark', 'auto'])),
            'notifications': draw(st.booleans()),
            'privacy_level': draw(st.integers(min_value=1, max_value=5))
        }
    }

@st.composite
def file_data(draw):
    """Generate file data for testing"""
    return {
        'filename': draw(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')))),
        'content': draw(st.binary(min_size=1, max_size=10000)),
        'content_type': draw(st.sampled_from(['text/plain', 'application/pdf', 'image/jpeg', 'application/json']))
    }

class SecurityStateMachine(RuleBasedStateMachine):
    """Stateful testing for comprehensive data security"""
    
    def __init__(self):
        super().__init__()
        self.security_service = SecurityService()
        self.cleanup_service = CleanupService()
        self.encrypted_data = {}
        self.user_files = {}
        self.user_sessions = {}
        self.temp_files = []
        
    @initialize()
    def setup(self):
        """Initialize test environment"""
        self.test_dir = tempfile.mkdtemp()
        os.environ['MASTER_KEY_FILE'] = os.path.join(self.test_dir, '.test_master_key')
        
    @rule(user_data=user_data())
    def encrypt_user_data(self, user_data):
        """Test encryption of user data"""
        user_id = user_data['user_id']
        
        # Test password hashing
        hashed_password = self.security_service.hash_password(user_data['password'])
        assert hashed_password != user_data['password']
        assert self.security_service.verify_password(user_data['password'], hashed_password)
        
        # Test data encryption
        sensitive_json = json.dumps(user_data['sensitive_data'])
        encrypted_metadata = self.security_service.encrypt_data(sensitive_json, user_data['password'])
        
        # Store for later verification
        self.encrypted_data[user_id] = {
            'original': sensitive_json,
            'encrypted': encrypted_metadata,
            'password': user_data['password']
        }
        
        # Verify encryption properties
        assert encrypted_metadata['algorithm'] == 'AES-256-GCM'
        assert 'encrypted_data' in encrypted_metadata
        assert encrypted_metadata['encrypted_data'] != sensitive_json
        
    @rule(user_id=st.text(min_size=8, max_size=32))
    def decrypt_user_data(self, user_id):
        """Test decryption of user data"""
        assume(user_id in self.encrypted_data)
        
        stored_data = self.encrypted_data[user_id]
        
        # Test successful decryption
        decrypted = self.security_service.decrypt_data(
            stored_data['encrypted'], 
            stored_data['password']
        )
        assert decrypted == stored_data['original']
        
        # Test failed decryption with wrong password
        with pytest.raises(SecurityException):
            self.security_service.decrypt_data(
                stored_data['encrypted'], 
                'wrong_password'
            )
        
    @rule(file_data=file_data(), user_password=st.text(min_size=8, max_size=32))
    def encrypt_file_data(self, file_data, user_password):
        """Test file encryption"""
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_data['filename']}")
        temp_file.write(file_data['content'])
        temp_file.close()
        self.temp_files.append(temp_file.name)
        
        # Encrypt file
        encrypted_metadata = self.security_service.encrypt_file(temp_file.name, user_password)
        
        # Store for verification
        file_id = f"file_{len(self.user_files)}"
        self.user_files[file_id] = {
            'original_path': temp_file.name,
            'original_content': file_data['content'],
            'encrypted_metadata': encrypted_metadata,
            'password': user_password
        }
        
        # Verify encryption properties
        assert encrypted_metadata['original_filename'] == os.path.basename(temp_file.name)
        assert encrypted_metadata['file_size'] == len(file_data['content'])
        assert 'encrypted_data' in encrypted_metadata
        
    @rule(file_id=st.text(min_size=1, max_size=20))
    def decrypt_file_data(self, file_id):
        """Test file decryption"""
        assume(file_id in self.user_files)
        
        file_info = self.user_files[file_id]
        
        # Create output file
        output_file = tempfile.NamedTemporaryFile(delete=False)
        output_file.close()
        self.temp_files.append(output_file.name)
        
        # Decrypt file
        decrypted_path = self.security_service.decrypt_file(
            file_info['encrypted_metadata'],
            output_file.name,
            file_info['password']
        )
        
        # Verify decryption
        with open(decrypted_path, 'rb') as f:
            decrypted_content = f.read()
        
        assert decrypted_content == file_info['original_content']
        
    @rule(user_data=user_data())
    def create_secure_token(self, user_data):
        """Test JWT token creation and verification"""
        user_id = user_data['user_id']
        
        # Create token
        payload = {
            'user_id': user_id,
            'email': user_data['email'],
            'permissions': ['read', 'write']
        }
        
        token = self.security_service.create_secure_token(payload, expires_hours=1)
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token
        decoded_payload = self.security_service.verify_token(token)
        assert decoded_payload['user_id'] == user_id
        assert decoded_payload['email'] == user_data['email']
        assert 'exp' in decoded_payload
        assert 'iat' in decoded_payload
        
        # Store for session testing
        self.user_sessions[user_id] = {
            'token': token,
            'payload': payload
        }
        
    @rule(user_id=st.text(min_size=8, max_size=32))
    def test_secure_deletion(self, user_id):
        """Test secure data deletion"""
        assume(user_id in self.encrypted_data or user_id in self.user_sessions)
        
        # Test secure data clearing
        if user_id in self.encrypted_data:
            data_dict = self.encrypted_data[user_id].copy()
            cleared_dict = self.security_service.secure_delete_data(data_dict)
            
            # Verify data is cleared
            for key, value in cleared_dict.items():
                if isinstance(value, str):
                    assert value != data_dict[key]
                else:
                    assert value is None
        
        # Test file deletion
        test_file = tempfile.NamedTemporaryFile(delete=False)
        test_file.write(b"sensitive data to delete")
        test_file.close()
        self.temp_files.append(test_file.name)
        
        # Verify file exists
        assert os.path.exists(test_file.name)
        
        # Secure delete
        success = self.security_service.secure_delete_file(test_file.name)
        assert success
        assert not os.path.exists(test_file.name)
        
    @rule(malicious_input=st.text(min_size=1, max_size=1000))
    def test_input_sanitization(self, malicious_input):
        """Test input sanitization against injection attacks"""
        # Test sanitization
        sanitized = self.security_service.sanitize_input(malicious_input)
        
        # Verify dangerous characters are removed
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00', '\n', '\r', '\t']
        for char in dangerous_chars:
            assert char not in sanitized
        
        # Verify length limit
        assert len(sanitized) <= 1000
        
    @rule(email=st.emails())
    def test_email_validation(self, email):
        """Test email validation"""
        is_valid = self.security_service.validate_email(email)
        assert isinstance(is_valid, bool)
        
        # Valid emails should pass
        if '@' in email and '.' in email.split('@')[1]:
            assert is_valid
            
    @invariant()
    def verify_security_invariants(self):
        """Verify security invariants are maintained"""
        # 1. All encrypted data should be different from original
        for user_id, data in self.encrypted_data.items():
            encrypted_str = data['encrypted']['encrypted_data']
            assert encrypted_str != data['original']
            
        # 2. All tokens should be valid format
        for user_id, session in self.user_sessions.items():
            token = session['token']
            assert isinstance(token, str)
            assert len(token.split('.')) == 3  # JWT format
            
        # 3. Master key should exist and be secure
        master_key_file = os.environ.get('MASTER_KEY_FILE')
        if master_key_file and os.path.exists(master_key_file):
            # Check file permissions (on Unix systems)
            if hasattr(os, 'stat'):
                stat_info = os.stat(master_key_file)
                # Should not be world-readable
                assert not (stat_info.st_mode & 0o004)
                
    def teardown(self):
        """Clean up test environment"""
        # Clean up temporary files
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        # Clean up test directory
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir, ignore_errors=True)

# Property-based tests
@given(user_data=user_data())
@settings(max_examples=100, deadline=None)
def test_encryption_roundtrip_property(user_data):
    """Property: Encryption and decryption should be perfect inverses"""
    security_service = SecurityService()
    
    # Test data encryption roundtrip
    original_data = json.dumps(user_data['sensitive_data'])
    encrypted_metadata = security_service.encrypt_data(original_data, user_data['password'])
    decrypted_data = security_service.decrypt_data(encrypted_metadata, user_data['password'])
    
    assert decrypted_data == original_data

@given(password=st.text(min_size=8, max_size=128))
@settings(max_examples=100)
def test_password_hashing_property(password):
    """Property: Password hashing should be deterministic and verifiable"""
    security_service = SecurityService()
    
    # Hash password
    hashed1 = security_service.hash_password(password)
    hashed2 = security_service.hash_password(password)
    
    # Hashes should be different (due to salt) but both should verify
    assert hashed1 != hashed2
    assert security_service.verify_password(password, hashed1)
    assert security_service.verify_password(password, hashed2)
    
    # Wrong password should not verify
    assert not security_service.verify_password(password + "wrong", hashed1)

@given(payload=st.dictionaries(st.text(min_size=1, max_size=20), st.text(min_size=1, max_size=100)))
@settings(max_examples=50)
def test_jwt_token_property(payload):
    """Property: JWT tokens should encode and decode consistently"""
    security_service = SecurityService()
    
    # Create and verify token
    token = security_service.create_secure_token(payload, expires_hours=1)
    decoded_payload = security_service.verify_token(token)
    
    # Original payload should be preserved
    for key, value in payload.items():
        assert decoded_payload[key] == value
    
    # Security claims should be added
    assert 'exp' in decoded_payload
    assert 'iat' in decoded_payload
    assert 'iss' in decoded_payload
    assert decoded_payload['iss'] == 'visionary-ai'

# Stateful testing
SecurityTest = SecurityStateMachine.TestCase

if __name__ == "__main__":
    # Run property tests
    test_encryption_roundtrip_property()
    test_password_hashing_property()
    test_jwt_token_property()
    
    # Run stateful tests
    pytest.main([__file__, "-v", "--tb=short"])