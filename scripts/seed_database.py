import sys
import os

# Get project root (parent of scripts directory)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root and backend to sys.path
backend_dir = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_dir)   # for app module
sys.path.insert(0, project_root)  # for payments, ai, ml, etc.

# Now import all required modules dynamically so Python resolves them at runtime
# based on the sys.path setup above without triggering static import-analysis errors.
import importlib

database_module = importlib.import_module('app.database.database')
seed_module = importlib.import_module('app.database.seed')

Base = database_module.Base
engine = database_module.engine
SessionLocal = database_module.SessionLocal
seed_database = seed_module.seed_database

# Create tables and seed data
Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_database(db)
db.close()
print("Database seeded successfully.")