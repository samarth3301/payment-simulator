from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Production database URL
DATABASE_URL = 'postgresql://neondb_owner:npg_gJLj7dthbBF4@ep-bold-morning-a18z1kqy-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()
        if version:
            print("Connection successful!")
            print(f"PostgreSQL version: {version[0]}")
        else:
            print("Connection successful, but no version returned.")
except SQLAlchemyError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")