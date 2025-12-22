#!/usr/bin/env python3
"""
Database initialization script for Visionary AI
This script creates all the required database tables
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import init_db, engine
from sqlalchemy import text

async def main():
    """Initialize the database with all required tables"""
    print("🚀 Initializing Visionary AI Database...")
    
    try:
        # Test database connection
        print("📡 Testing database connection...")
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Initialize all tables
        print("🏗️  Creating database tables...")
        await init_db()
        print("✅ All database tables created successfully!")
        
        # Verify tables were created
        print("🔍 Verifying tables...")
        async with engine.begin() as conn:
            # Check if users table exists
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
            if result.fetchone():
                print("✅ Users table created")
            else:
                print("❌ Users table not found")
            
            # List all tables
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Created tables: {', '.join(tables)}")
        
        print("\n🎉 Database initialization completed successfully!")
        print("🚀 You can now start your backend server and use the app!")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    finally:
        await engine.dispose()
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)