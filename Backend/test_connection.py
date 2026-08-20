from apps.database import engine

with engine.connect() as conn:
    print("✅ Connected to Postgres successfully!")