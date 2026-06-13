"""
Simple script to show database tables and data
Run from backend directory: python show_database.py
"""
import sys
from pathlib import Path

# Add parent directory to Python path (same as run_server.py)
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from sqlalchemy import inspect, text
from backend.database.connection import engine, SessionLocal, init_db
from backend.database.models import Incident, RCAReport, KnowledgeBase, SimilarIncident

print("="*60)
print("  DATABASE DEMONSTRATION")
print("="*60)

# Initialize database
print("\n1. Initializing database...")
init_db()
print("   ✅ Database initialized")

# Show tables
print("\n2. Tables in database:")
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"   Total tables: {len(tables)}")
for table in tables:
    print(f"   - {table}")

# Show table structures
print("\n3. Table structures:")
for table in tables:
    print(f"\n   Table: {table}")
    columns = inspector.get_columns(table)
    print(f"   Columns: {len(columns)}")
    for col in columns:
        print(f"     • {col['name']}: {col['type']}")

# Show data counts
print("\n4. Data in tables:")
db = SessionLocal()
try:
    incident_count = db.query(Incident).count()
    rca_count = db.query(RCAReport).count()
    kb_count = db.query(KnowledgeBase).count()
    similar_count = db.query(SimilarIncident).count()
    
    print(f"   Incidents: {incident_count} records")
    print(f"   RCA Reports: {rca_count} records")
    print(f"   Knowledge Base: {kb_count} records")
    print(f"   Similar Incidents: {similar_count} records")
    
    # Show sample incident if exists
    if incident_count > 0:
        sample = db.query(Incident).first()
        print(f"\n5. Sample incident:")
        print(f"   ID: {sample.id}")
        print(f"   Title: {sample.title}")
        print(f"   Severity: {sample.severity}")
        print(f"   Status: {sample.status}")
        print(f"   Created: {sample.created_at}")
finally:
    db.close()

print("\n" + "="*60)
print("  ✅ DATABASE IS WORKING!")
print("="*60)
