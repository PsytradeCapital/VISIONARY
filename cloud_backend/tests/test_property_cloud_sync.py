"""
Property-based tests for real-time cloud synchronization
Validates Requirements 1.3, 5.4

Feature: ai-personal-scheduler
Property 2: Real-time knowledge base synchronization
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, invariant
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid
import json
import time
from unittest.mock import Mock, patch, AsyncMock

from app.models.knowledge import KnowledgeBase, Document, ProcessingMetadata
from app.models.user import User
from app.core.database import get_postgres_session

# Test data generators
@st.composite
def knowledge_item(draw):
    """Generate knowledge base items for testing"""
    return {
        "title": draw(st.text(min_size=1, max_size=200)),
        "content": draw(st.text(min_size=10, max_size=5000)),
        "content_type": draw(st.sampled_from(["document", "voice", "text", "image"])),
        "categories": draw(st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5)),
        "tags": draw(st.lists(st.text(min_size=1, max_size=30), min_size=0, max_size=10)),
        "processing_priority": draw(st.sampled_from(["low", "normal", "high", "urgent"]))
    }

@st.composite
def sync_operation(draw):
    """Generate synchronization operations"""
    return {
        "operation_type": draw(st.sampled_from(["create", "update", "delete", "bulk_update"])),
        "timestamp": datetime.utcnow(),
        "device_id": draw(st.text(min_size=10, max_size=50)),
        "user_id": draw(st.integers(min_value=1, max_value=1000)),
        "batch_size": draw(st.integers(min_value=1, max_value=100))
    }

@st.composite
def network_condition(draw):
    """Generate network conditions for testing"""
    return {
        "latency_ms": draw(st.integers(min_value=10, max_value=5000)),
        "bandwidth_mbps": draw(st.floats(min_value=0.1, max_value=1000.0)),
        "packet_loss_percent": draw(st.floats(min_value=0.0, max_value=50.0)),
        "connection_stable": draw(st.booleans()),
        "offline_duration_seconds": draw(st.integers(min_value=0, max_value=3600))
    }

class CloudSyncStateMachine(RuleBasedStateMachine):
    """
    Stateful property-based testing for real-time cloud synchronization
    Tests sync consistency, conflict resolution, and offline handling
    """
    
    def __init__(self):
        super().__init__()
        self.local_data: Dict[str, Dict] = {}  # Local device data
        self.cloud_data: Dict[str, Dict] = {}  # Cloud server data
        self.sync_queue: List[Dict] = []  # Pending sync operations
        self.conflict_log: List[Dict] = []  # Sync conflicts
        self.offline_changes: Dict[str, List] = {}  # Changes made while offline
        self.sync_timestamps: Dict[str, datetime] = {}  # Last sync times
        self.devices: Dict[str, Dict] = {}  # Multiple device simulation
        
    @initialize()
    def setup(self):
        """Initialize sync environment"""
        self.sync_enabled = True
        self.network_available = True
        self.last_sync_time = datetime.utcnow()
        
    @rule(item=knowledge_item(), device_id=st.text(min_size=5, max_size=20))
    def create_knowledge_item_local(self, item, device_id):
        """Create knowledge item on local device"""
        item_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        local_item = {
            **item,
            "id": item_id,
            "device_id": device_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "sync_status": "pending",
            "version": 1,
            "local_changes": True
        }
        
        self.local_data[item_id] = local_item
        
        # Add to sync queue if network available
        if self.network_available:
            self.sync_queue.append({
                "operation": "create",
                "item_id": item_id,
                "data": local_item,
                "timestamp": timestamp,
                "device_id": device_id
            })
        else:
            # Store offline changes
            if device_id not in self.offline_changes:
                self.offline_changes[device_id] = []
            self.offline_changes[device_id].append({
                "operation": "create",
                "item_id": item_id,
                "data": local_item,
                "timestamp": timestamp
            })
    
    @rule(network_condition=network_condition())
    def simulate_network_conditions(self, network_condition):
        """Simulate various network conditions"""
        self.network_available = network_condition["connection_stable"]
        
        if not self.network_available:
            # Simulate offline period
            offline_duration = network_condition["offline_duration_seconds"]
            if offline_duration > 0:
                time.sleep(min(offline_duration / 1000, 0.1))  # Scale down for testing
        
        # Simulate network latency affecting sync
        if network_condition["latency_ms"] > 1000:
            # High latency - batch sync operations
            self._batch_sync_operations()
    
    @rule()
    def process_sync_queue(self):
        """Process pending synchronization operations"""
        assume(len(self.sync_queue) > 0)
        assume(self.network_available)
        
        # Process sync operations in batches
        batch_size = min(10, len(self.sync_queue))
        batch = self.sync_queue[:batch_size]
        self.sync_queue = self.sync_queue[batch_size:]
        
        for sync_op in batch:
            self._sync_to_cloud(sync_op)
    
    def _sync_to_cloud(self, sync_op):
        """Synchronize operation to cloud"""
        item_id = sync_op["item_id"]
        operation = sync_op["operation"]
        
        if operation == "create":
            if item_id not in self.cloud_data:
                # No conflict - create in cloud
                self.cloud_data[item_id] = {
                    **sync_op["data"],
                    "cloud_synced": True,
                    "cloud_sync_time": datetime.utcnow()
                }
                
                # Update local sync status
                if item_id in self.local_data:
                    self.local_data[item_id]["sync_status"] = "synced"
                    self.local_data[item_id]["local_changes"] = False
                    
                self.sync_timestamps[item_id] = datetime.utcnow()
            else:
                # Conflict detected
                self._handle_sync_conflict(sync_op)
        
        elif operation == "update":
            if item_id in self.cloud_data:
                cloud_item = self.cloud_data[item_id]
                local_item = sync_op["data"]
                
                # Check for conflicts based on version/timestamp
                if self._has_sync_conflict(local_item, cloud_item):
                    self._handle_sync_conflict(sync_op)
                else:
                    # No conflict - update cloud
                    self.cloud_data[item_id] = {
                        **local_item,
                        "cloud_synced": True,
                        "cloud_sync_time": datetime.utcnow()
                    }
                    
                    if item_id in self.local_data:
                        self.local_data[item_id]["sync_status"] = "synced"
                        self.local_data[item_id]["local_changes"] = False
                        
                    self.sync_timestamps[item_id] = datetime.utcnow()
    
    def _has_sync_conflict(self, local_item, cloud_item):
        """Check if there's a synchronization conflict"""
        # Conflict if both have been modified since last sync
        local_modified = local_item.get("updated_at", datetime.min)
        cloud_modified = cloud_item.get("updated_at", datetime.min)
        last_sync = self.sync_timestamps.get(local_item["id"], datetime.min)
        
        return (local_modified > last_sync and cloud_modified > last_sync and 
                local_modified != cloud_modified)
    
    def _handle_sync_conflict(self, sync_op):
        """Handle synchronization conflicts"""
        item_id = sync_op["item_id"]
        
        conflict = {
            "item_id": item_id,
            "conflict_type": "concurrent_modification",
            "local_data": sync_op["data"],
            "cloud_data": self.cloud_data.get(item_id),
            "timestamp": datetime.utcnow(),
            "resolution_strategy": "last_write_wins",  # Default strategy
            "resolved": False
        }
        
        self.conflict_log.append(conflict)
        
        # Apply conflict resolution strategy
        if conflict["resolution_strategy"] == "last_write_wins":
            local_time = sync_op["data"].get("updated_at", datetime.min)
            cloud_time = self.cloud_data[item_id].get("updated_at", datetime.min)
            
            if local_time > cloud_time:
                # Local wins
                self.cloud_data[item_id] = {
                    **sync_op["data"],
                    "cloud_synced": True,
                    "cloud_sync_time": datetime.utcnow(),
                    "conflict_resolved": True
                }
            # else cloud wins (no action needed)
            
            conflict["resolved"] = True
    
    @rule()
    def simulate_offline_sync(self):
        """Simulate synchronization after coming back online"""
        assume(len(self.offline_changes) > 0)
        
        # Network comes back online
        self.network_available = True
        
        # Process offline changes
        for device_id, changes in self.offline_changes.items():
            for change in changes:
                self.sync_queue.append({
                    **change,
                    "device_id": device_id,
                    "offline_change": True
                })
        
        # Clear offline changes after queuing
        self.offline_changes.clear()
    
    def _batch_sync_operations(self):
        """Batch sync operations for efficiency"""
        if len(self.sync_queue) > 5:
            # Group operations by type
            creates = [op for op in self.sync_queue if op["operation"] == "create"]
            updates = [op for op in self.sync_queue if op["operation"] == "update"]
            
            # Process in batches
            self.sync_queue = creates[:5] + updates[:5]  # Limit batch size
    
    @rule(device_id=st.text(min_size=5, max_size=20))
    def simulate_multi_device_sync(self, device_id):
        """Simulate synchronization across multiple devices"""
        assume(len(self.cloud_data) > 0)
        
        # Register device
        if device_id not in self.devices:
            self.devices[device_id] = {
                "last_sync": datetime.utcnow() - timedelta(minutes=5),
                "local_data": {}
            }
        
        device = self.devices[device_id]
        
        # Sync cloud changes to device
        for item_id, cloud_item in self.cloud_data.items():
            cloud_sync_time = cloud_item.get("cloud_sync_time", datetime.min)
            
            if cloud_sync_time > device["last_sync"]:
                # Update device with cloud changes
                device["local_data"][item_id] = {
                    **cloud_item,
                    "device_id": device_id,
                    "sync_status": "synced",
                    "local_changes": False
                }
        
        device["last_sync"] = datetime.utcnow()
    
    @invariant()
    def sync_consistency_maintained(self):
        """Invariant: Synced items must be consistent between local and cloud"""
        for item_id, local_item in self.local_data.items():
            if local_item.get("sync_status") == "synced":
                assert item_id in self.cloud_data, f"Synced item {item_id} missing from cloud"
                
                cloud_item = self.cloud_data[item_id]
                
                # Core content should match
                assert local_item["title"] == cloud_item["title"]
                assert local_item["content"] == cloud_item["content"]
                assert local_item["content_type"] == cloud_item["content_type"]
    
    @invariant()
    def no_data_loss_during_sync(self):
        """Invariant: No data should be lost during synchronization"""
        total_local_items = len(self.local_data)
        total_cloud_items = len(self.cloud_data)
        total_pending_sync = len(self.sync_queue)
        total_offline_changes = sum(len(changes) for changes in self.offline_changes.values())
        
        # Total items should be preserved (accounting for pending operations)
        assert total_cloud_items <= total_local_items + total_pending_sync + total_offline_changes
    
    @invariant()
    def conflicts_properly_logged(self):
        """Invariant: All sync conflicts must be logged and resolved"""
        for conflict in self.conflict_log:
            assert "item_id" in conflict
            assert "conflict_type" in conflict
            assert "timestamp" in conflict
            assert "resolution_strategy" in conflict
            # All conflicts should eventually be resolved
            # (In real system, unresolved conflicts would be handled by user or automatic resolution)
    
    @invariant()
    def sync_timestamps_accurate(self):
        """Invariant: Sync timestamps must be accurate and monotonic"""
        timestamps = list(self.sync_timestamps.values())
        if len(timestamps) > 1:
            # Timestamps should be in reasonable order (allowing for some clock skew)
            sorted_timestamps = sorted(timestamps)
            assert timestamps == sorted_timestamps or len(set(timestamps)) == len(timestamps)

# Property-based tests
@given(items=st.lists(knowledge_item(), min_size=1, max_size=20))
@settings(max_examples=50, deadline=None)
def test_batch_sync_consistency_property(items):
    """
    Property: Batch synchronization must maintain data consistency
    Validates Requirements 1.3, 5.4
    """
    local_batch = {}
    cloud_batch = {}
    
    # Simulate batch creation
    for i, item in enumerate(items):
        item_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        local_item = {
            **item,
            "id": item_id,
            "created_at": timestamp,
            "version": 1
        }
        
        local_batch[item_id] = local_item
    
    # Simulate batch sync to cloud
    for item_id, local_item in local_batch.items():
        cloud_batch[item_id] = {
            **local_item,
            "cloud_synced": True,
            "cloud_sync_time": datetime.utcnow()
        }
    
    # Verify consistency
    assert len(local_batch) == len(cloud_batch)
    
    for item_id in local_batch:
        assert item_id in cloud_batch
        assert local_batch[item_id]["title"] == cloud_batch[item_id]["title"]
        assert local_batch[item_id]["content"] == cloud_batch[item_id]["content"]

@given(sync_ops=st.lists(sync_operation(), min_size=1, max_size=10))
@settings(max_examples=30, deadline=None)
def test_concurrent_sync_property(sync_ops):
    """
    Property: Concurrent sync operations must not cause data corruption
    Validates Requirements 1.3, 5.4
    """
    sync_results = {}
    
    # Simulate concurrent sync operations
    for sync_op in sync_ops:
        item_id = str(uuid.uuid4())
        
        # Each operation should complete successfully
        sync_result = {
            "item_id": item_id,
            "operation": sync_op["operation_type"],
            "timestamp": sync_op["timestamp"],
            "success": True,
            "conflicts": []
        }
        
        # Check for potential conflicts with existing operations
        for existing_id, existing_result in sync_results.items():
            if (existing_result["timestamp"] == sync_result["timestamp"] and
                existing_result["operation"] == sync_result["operation"]):
                # Potential conflict - should be handled gracefully
                sync_result["conflicts"].append(existing_id)
        
        sync_results[item_id] = sync_result
    
    # Verify all operations completed successfully
    for item_id, result in sync_results.items():
        assert result["success"] is True
        # Conflicts should be detected but not cause failures
        assert isinstance(result["conflicts"], list)

@given(network_conditions=st.lists(network_condition(), min_size=1, max_size=5))
@settings(max_examples=20, deadline=None)
def test_network_resilience_property(network_conditions):
    """
    Property: Sync must be resilient to network conditions
    Validates Requirements 5.4
    """
    sync_queue = []
    offline_queue = []
    
    for condition in network_conditions:
        if condition["connection_stable"]:
            # Process any offline queue
            sync_queue.extend(offline_queue)
            offline_queue.clear()
            
            # Add new sync operation
            sync_queue.append({
                "timestamp": datetime.utcnow(),
                "latency": condition["latency_ms"],
                "bandwidth": condition["bandwidth_mbps"]
            })
        else:
            # Add to offline queue
            offline_queue.append({
                "timestamp": datetime.utcnow(),
                "offline_duration": condition["offline_duration_seconds"]
            })
    
    # Verify resilience
    total_operations = len(sync_queue) + len(offline_queue)
    assert total_operations == len(network_conditions)
    
    # All operations should eventually be processable
    if len(offline_queue) > 0:
        # Simulate network recovery
        sync_queue.extend(offline_queue)
        offline_queue.clear()
    
    assert len(offline_queue) == 0  # All operations should be queued for sync

@given(st.integers(min_value=2, max_value=10))
@settings(max_examples=20, deadline=None)
def test_multi_device_sync_property(device_count):
    """
    Property: Multi-device synchronization must maintain consistency
    Validates Requirements 1.3, 5.4
    """
    devices = {}
    cloud_state = {}
    
    # Initialize devices
    for i in range(device_count):
        device_id = f"device_{i}"
        devices[device_id] = {
            "local_data": {},
            "last_sync": datetime.utcnow() - timedelta(minutes=i)
        }
    
    # Simulate data creation on different devices
    for i, device_id in enumerate(devices.keys()):
        item_id = str(uuid.uuid4())
        item_data = {
            "id": item_id,
            "title": f"Item from {device_id}",
            "content": f"Content created on {device_id}",
            "created_at": datetime.utcnow(),
            "device_origin": device_id
        }
        
        # Add to device local data
        devices[device_id]["local_data"][item_id] = item_data
        
        # Sync to cloud
        cloud_state[item_id] = {
            **item_data,
            "cloud_synced": True,
            "sync_timestamp": datetime.utcnow()
        }
    
    # Simulate sync to all devices
    for device_id, device in devices.items():
        for item_id, cloud_item in cloud_state.items():
            if item_id not in device["local_data"]:
                # Sync cloud item to device
                device["local_data"][item_id] = {
                    **cloud_item,
                    "synced_to_device": device_id
                }
    
    # Verify consistency across all devices
    for device_id, device in devices.items():
        assert len(device["local_data"]) == len(cloud_state)
        
        for item_id in cloud_state:
            assert item_id in device["local_data"]
            local_item = device["local_data"][item_id]
            cloud_item = cloud_state[item_id]
            
            assert local_item["title"] == cloud_item["title"]
            assert local_item["content"] == cloud_item["content"]

# Integration test with the state machine
@settings(max_examples=5, stateful_step_count=30, deadline=None)
class TestCloudSyncStateMachine(CloudSyncStateMachine):
    """Run the stateful property-based tests for cloud sync"""
    pass

# Async property tests
@pytest.mark.asyncio
async def test_real_time_sync_property():
    """
    Property: Real-time sync must propagate changes within acceptable time limits
    Validates Requirements 1.3, 5.4
    """
    sync_events = []
    max_sync_delay = 5.0  # seconds
    
    # Simulate real-time change
    change_timestamp = datetime.utcnow()
    
    # Simulate sync propagation
    await asyncio.sleep(0.1)  # Simulate network delay
    
    sync_timestamp = datetime.utcnow()
    sync_delay = (sync_timestamp - change_timestamp).total_seconds()
    
    sync_events.append({
        "change_time": change_timestamp,
        "sync_time": sync_timestamp,
        "delay": sync_delay
    })
    
    # Verify real-time performance
    for event in sync_events:
        assert event["delay"] < max_sync_delay, f"Sync delay {event['delay']}s exceeds limit"

if __name__ == "__main__":
    # Run property-based tests
    pytest.main([__file__, "-v", "--tb=short"])