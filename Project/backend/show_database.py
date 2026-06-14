import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Add the current directory to path so database imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import settings, init_db
from database.models import Base, Incident, RCAReport, KnowledgeBase, SimilarIncident

def show_database_structure():
    print("=" * 60)
    print("  DATABASE DEMONSTRATION")
    print("=" * 60)
    
    print("\n1. Initializing database...")
    db_success = init_db()
    if db_success:
        print("   [OK] Database initialized")
    else:
        print("   [ERROR] Database initialization failed")
        return

    print(f"\nDatabase URL: {settings.DATABASE_URL}")
    
    # Create engine and inspector
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)
    
    # Get table names
    tables = inspector.get_table_names()
    print(f"\n2. Tables in database:")
    print(f"   Total tables: {len(tables)}")
    for table in tables:
        print(f"   - {table}")
        
    print("\n3. Table structures:")
    for table_name in tables:
        print(f"\n   Table: {table_name}")
        columns = inspector.get_columns(table_name)
        print(f"   Columns: {len(columns)}")
        for col in columns:
            col_type = str(col['type'])
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            pk = "PRIMARY KEY" if col.get('primary_key') else ""
            fk = f"FOREIGN KEY -> {col.get('foreign_key')}" if col.get('foreign_key') else ""
            info = ", ".join(filter(None, [col_type, nullable, pk, fk]))
            print(f"     * {col['name']}: {info}")
            
    # Connect session to read counts
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        incidents_count = session.query(Incident).count()
        rca_count = session.query(RCAReport).count()
        kb_count = session.query(KnowledgeBase).count()
        similar_count = session.query(SimilarIncident).count()
        
        print("\n4. Data in tables:")
        print(f"   Incidents: {incidents_count} records")
        print(f"   RCA Reports: {rca_count} records")
        print(f"   Knowledge Base: {kb_count} records")
        print(f"   Similar Incidents: {similar_count} records")
    except Exception as e:
        print(f"\n[ERROR] Error reading data: {e}")
    finally:
        session.close()

    print("\n" + "=" * 60)
    print("  [OK] DATABASE IS WORKING!")
    print("=" * 60)

if __name__ == "__main__":
    show_database_structure()
