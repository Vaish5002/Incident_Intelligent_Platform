"""
Test Suite for Module 5 (Knowledge Base) and Module 6 (Embedding Service)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ai.knowledge_base import KnowledgeBaseService
from backend.ai.embedding_service import EmbeddingService
from backend.database.connection import init_db


def print_header(text):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def print_success(text):
    print(f"SUCCESS: {text}")


def print_test(text):
    print(f"\n--- {text} ---")


def test_module5_knowledge_base():
    """Test Module 5: Knowledge Base"""
    print_header("MODULE 5: KNOWLEDGE BASE")
    
    # Initialize database
    print("Initializing database...")
    init_success = init_db()
    assert init_success, "Failed to initialize database"
    print("Database initialized successfully")
    
    kb_service = KnowledgeBaseService()
    print("Knowledge base service initialized")
    
    # Test 1: Insert record (Expected: Stored successfully)
    print_test("Test 1: Insert Incident Record")
    
    result1 = kb_service.store_incident(
        incident_id="INC-TEST-001",
        description="Database connection timeout causing payment failures",
        severity="Critical",
        affected_service="payment",
        risk_score=85.5,
        confidence=90.0,
        metadata={
            "deployment": "v2.1.0",
            "environment": "production"
        }
    )
    
    print(f"Store Result: {result1}")
    print(f"  Success: {result1['success']}")
    print(f"  Incident ID: {result1.get('incident_id')}")
    print(f"  Created At: {result1.get('created_at')}")
    
    # Verify Test 1
    assert result1['success'], "Failed to store incident"
    assert result1['incident_id'] == "INC-TEST-001", "Incorrect incident ID"
    print_success("Test 1 PASSED - Record stored successfully")
    
    # Test 2: Retrieve record (Expected: Correct record returned)
    print_test("Test 2: Retrieve Incident Record")
    
    retrieved = kb_service.get_incident("INC-TEST-001")
    
    print(f"Retrieved Incident:")
    print(f"  ID: {retrieved['incident_id']}")
    print(f"  Description: {retrieved['description'][:60]}...")
    print(f"  Severity: {retrieved['severity']}")
    print(f"  Service: {retrieved['affected_service']}")
    print(f"  Risk Score: {retrieved['risk_score']}")
    print(f"  Status: {retrieved['status']}")
    
    # Verify Test 2
    assert retrieved is not None, "Failed to retrieve incident"
    assert retrieved['incident_id'] == "INC-TEST-001", "Wrong incident retrieved"
    assert retrieved['description'] == "Database connection timeout causing payment failures"
    assert retrieved['severity'] == "Critical"
    assert retrieved['affected_service'] == "payment"
    print_success("Test 2 PASSED - Correct record returned")
    
    # Test 3: Store RCA Report
    print_test("Test 3: Store RCA Report")
    
    rca_result = kb_service.store_rca_report(
        incident_id="INC-TEST-001",
        root_cause="Database pool size reduced from 50 to 10 in recent deployment",
        impact_analysis="Complete payment service outage for 45 minutes",
        recommendations="1. Increase pool size\n2. Add monitoring\n3. Implement gradual rollout",
        prevention_measures="Add configuration validation in CI/CD pipeline",
        rca_text="# Root Cause Analysis\n\n## Summary\nDatabase misconfiguration...",
        model_used="llama-3.3-70b-versatile",
        root_cause_candidates=[
            {"type": "config_change", "confidence": 0.9, "description": "Pool size reduction"}
        ]
    )
    
    print(f"RCA Store Result: {rca_result}")
    assert rca_result['success'], "Failed to store RCA report"
    print_success("Test 3 PASSED - RCA report stored")
    
    # Test 4: Store Knowledge Entry
    print_test("Test 4: Store Knowledge Entry")
    
    entry_result = kb_service.store_knowledge_entry(
        incident_id="INC-TEST-001",
        entry_type="root_cause",
        title="Database Pool Configuration Issue",
        content="Reducing database pool size below load requirements causes connection exhaustion",
        tags=["database", "configuration", "performance"]
    )
    
    print(f"Entry Store Result: {entry_result}")
    assert entry_result['success'], "Failed to store knowledge entry"
    print_success("Test 4 PASSED - Knowledge entry stored")
    
    # Test 5: List incidents
    print_test("Test 5: List All Incidents")
    
    incidents = kb_service.get_all_incidents(limit=10)
    print(f"Found {len(incidents)} incidents")
    for inc in incidents:
        print(f"  - {inc['incident_id']}: {inc['description'][:50]}...")
    
    assert len(incidents) > 0, "No incidents found"
    print_success("Test 5 PASSED - Incidents listed successfully")
    
    print_header("MODULE 5: ALL TESTS PASSED")
    return True


def test_module6_embedding_service():
    """Test Module 6: Embedding Service"""
    print_header("MODULE 6: EMBEDDING SERVICE")
    
    embedding_service = EmbeddingService()
    print("Embedding service initialized")
    
    # Test 1: Generate embedding (Expected: Vector created)
    print_test("Test 1: Generate Embedding")
    
    text1 = "Database connection timeout causing payment failures"
    embedding1 = embedding_service.generate_embedding(text1)
    
    print(f"Text: {text1}")
    print(f"Embedding Generated:")
    print(f"  Dimensions: {len(embedding1)}")
    print(f"  Sample values: {embedding1[:5]}...")
    print(f"  Model: {embedding_service.model_name}")
    
    # Verify Test 1
    assert len(embedding1) > 0, "Embedding is empty"
    assert isinstance(embedding1, list), "Embedding is not a list"
    assert isinstance(embedding1[0], float), "Embedding values are not floats"
    print_success("Test 1 PASSED - Vector created successfully")
    
    # Test 2: Store embedding (save and load)
    print_test("Test 2: Store and Load Embedding")
    
    # Save to JSON
    json_str = embedding_service.save_to_json(embedding1)
    print(f"Embedding saved to JSON (length: {len(json_str)} chars)")
    
    # Load from JSON
    loaded_embedding = embedding_service.load_from_json(json_str)
    print(f"Embedding loaded from JSON")
    print(f"  Original dimensions: {len(embedding1)}")
    print(f"  Loaded dimensions: {len(loaded_embedding)}")
    print(f"  Match: {embedding1 == loaded_embedding}")
    
    # Verify Test 2
    assert loaded_embedding == embedding1, "Loaded embedding doesn't match original"
    print_success("Test 2 PASSED - Embedding saved and loaded successfully")
    
    # Test 3: Generate multiple embeddings
    print_test("Test 3: Batch Embedding Generation")
    
    texts = [
        "Database connection timeout",
        "Memory leak in application",
        "API gateway timeout",
        "Authentication failure"
    ]
    
    embeddings = embedding_service.generate_embeddings_batch(texts)
    
    print(f"Generated {len(embeddings)} embeddings")
    for i, text in enumerate(texts):
        print(f"  {i+1}. {text}: {len(embeddings[i])} dimensions")
    
    assert len(embeddings) == len(texts), "Wrong number of embeddings"
    print_success("Test 3 PASSED - Batch embeddings generated")
    
    # Test 4: Calculate similarity
    print_test("Test 4: Calculate Similarity")
    
    text_a = "Database connection timeout"
    text_b = "Database timeout error"
    text_c = "Memory leak detected"
    
    emb_a = embedding_service.generate_embedding(text_a)
    emb_b = embedding_service.generate_embedding(text_b)
    emb_c = embedding_service.generate_embedding(text_c)
    
    sim_ab = embedding_service.calculate_similarity(emb_a, emb_b)
    sim_ac = embedding_service.calculate_similarity(emb_a, emb_c)
    
    print(f"Text A: {text_a}")
    print(f"Text B: {text_b}")
    print(f"Text C: {text_c}")
    print(f"\nSimilarity A-B (similar): {sim_ab:.4f}")
    print(f"Similarity A-C (different): {sim_ac:.4f}")
    
    # Similar texts should have higher similarity
    assert sim_ab > sim_ac, "Similar texts don't have higher similarity"
    assert 0 <= sim_ab <= 1, "Similarity out of range"
    print_success("Test 4 PASSED - Similarity calculation working")
    
    # Test 5: Find similar items
    print_test("Test 5: Find Similar Items")
    
    query_text = "Payment service connection timeout"
    query_embedding = embedding_service.generate_embedding(query_text)
    
    candidate_texts = [
        "Database connection timeout",
        "API timeout error",
        "Memory leak issue",
        "Configuration error",
        "Network connectivity problem"
    ]
    
    candidate_embeddings = embedding_service.generate_embeddings_batch(candidate_texts)
    
    similar_items = embedding_service.find_similar(
        query_embedding,
        candidate_embeddings,
        top_k=3
    )
    
    print(f"Query: {query_text}")
    print(f"\nTop 3 Similar Items:")
    for item in similar_items:
        idx = item['index']
        similarity = item['similarity']
        print(f"  {idx+1}. {candidate_texts[idx]} (similarity: {similarity:.4f})")
    
    assert len(similar_items) > 0, "No similar items found"
    assert similar_items[0]['similarity'] >= similar_items[-1]['similarity'], "Results not sorted"
    print_success("Test 5 PASSED - Similar items found")
    
    # Test 6: Embed incident (complete workflow)
    print_test("Test 6: Embed Complete Incident")
    
    incident_embeddings = embedding_service.embed_incident(
        incident_description="Users unable to complete payment transactions",
        logs="Database timeout errors, connection pool exhausted",
        rca_text="Root cause: Database pool size reduced in recent deployment"
    )
    
    print(f"Generated embeddings for incident:")
    for key, embedding in incident_embeddings.items():
        print(f"  {key}: {len(embedding)} dimensions")
    
    assert "incident" in incident_embeddings, "Incident embedding missing"
    assert "logs" in incident_embeddings, "Logs embedding missing"
    assert "rca" in incident_embeddings, "RCA embedding missing"
    assert "combined" in incident_embeddings, "Combined embedding missing"
    print_success("Test 6 PASSED - Complete incident embedded")
    
    # Test 7: Get embedding info
    print_test("Test 7: Get Embedding Service Info")
    
    info = embedding_service.get_embedding_info()
    print(f"Embedding Service Info:")
    print(f"  Model: {info['model_name']}")
    print(f"  Is Fitted: {info['is_fitted']}")
    print(f"  Dimensions: {info['dimensions']}")
    print(f"  Vocabulary Size: {info['vocabulary_size']}")
    
    assert info['is_fitted'], "Service not fitted"
    print_success("Test 7 PASSED - Service info retrieved")
    
    print_header("MODULE 6: ALL TESTS PASSED")
    return True


def main():
    """Run all tests"""
    print_header("TESTING MODULE 5 & 6")
    print("Member 3: AI & RCA Engine")
    print("Testing Knowledge Base and Embedding Service")
    
    try:
        # Test Module 5
        module5_pass = test_module5_knowledge_base()
        
        # Test Module 6
        module6_pass = test_module6_embedding_service()
        
        # Final Summary
        print_header("FINAL TEST RESULTS")
        if module5_pass and module6_pass:
            print("SUCCESS: All tests passed!")
            print("\nModule 5: Knowledge Base - COMPLETE")
            print("  - Database tables created")
            print("  - Insert record -> Stored successfully")
            print("  - Retrieve record -> Correct record returned")
            print("  - RCA reports stored")
            print("  - Knowledge entries stored")
            print("\nModule 6: Embedding Service - COMPLETE")
            print("  - Generate embedding -> Vector created")
            print("  - Store embedding -> Saved successfully")
            print("  - Batch embeddings working")
            print("  - Similarity calculation working")
            print("  - Find similar items working")
            print("\nDeliverables:")
            print("  Module 5: Knowledge base ready")
            print("  Module 6: Embeddings working")
            print_header("ALL MODULES READY FOR PRODUCTION")
            return 0
        else:
            print("FAILURE: Some tests failed")
            return 1
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
