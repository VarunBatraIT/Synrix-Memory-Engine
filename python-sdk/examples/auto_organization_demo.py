#!/usr/bin/env python3
"""
Auto-Organization Demo
======================

Demonstrates SYNRIX's automatic organization system that classifies
and organizes data on ingestion without manual prefix assignment.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from synrix.raw_backend import RawSynrixBackend
from synrix.auto_organizer import classify_data


def demo_automatic_classification():
    """Demonstrate automatic classification"""
    print("=" * 70)
    print("SYNRIX Auto-Organization Demo")
    print("=" * 70)
    print()
    
    # Test cases
    test_cases = [
        {
            "data": "addition operation",
            "context": None,
            "description": "ISA/Instruction pattern"
        },
        {
            "data": "def calculate_sum(a, b): return a + b",
            "context": None,
            "description": "Code pattern"
        },
        {
            "data": "learned pattern: error handling in loops",
            "context": None,
            "description": "Learning pattern"
        },
        {
            "data": "constraint: no regex allowed",
            "context": None,
            "description": "Constraint pattern"
        },
        {
            "data": "user preference: Python over Java",
            "context": {"agent_id": "123"},
            "description": "Agent context"
        },
        {
            "data": "energy conservation in quantum systems",
            "context": None,
            "description": "Domain classification (physics)"
        },
        {
            "data": "molecular reaction rates",
            "context": None,
            "description": "Domain classification (chemistry)"
        },
        {
            "data": "arbitrary data without clear pattern",
            "context": None,
            "description": "Generic fallback"
        }
    ]
    
    print("📊 Classification Results:")
    print()
    
    for i, test in enumerate(test_cases, 1):
        result = classify_data(test["data"], test["context"])
        
        print(f"{i}. {test['description']}")
        print(f"   Data: {test['data'][:50]}...")
        print(f"   Prefix: {result.prefix}")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   Reason: {result.reason}")
        if result.suggested_name:
            print(f"   Suggested Name: {result.suggested_name}")
        print()
    
    print("=" * 70)
    print()


def demo_automatic_storage():
    """Demonstrate automatic storage with SYNRIX"""
    print("=" * 70)
    print("Automatic Storage Demo")
    print("=" * 70)
    print()
    
    # Initialize backend
    backend = RawSynrixBackend("auto_org_demo.lattice", max_nodes=10000, evaluation_mode=False)
    
    # Store data with automatic organization
    test_data = [
        ("addition operation", None),
        ("def calculate_sum(a, b): return a + b", None),
        ("learned pattern: error handling", None),
        ("user preference: Python", {"agent_id": "123"}),
        ("energy conservation formula", None),
    ]
    
    print("📝 Storing data with automatic organization...")
    print()
    
    node_ids = []
    for data, context in test_data:
        try:
            node_id = backend.add_node_auto(data, context=context)
            if node_id:
                node_ids.append(node_id)
                result = classify_data(data, context)
                print(f"✅ Stored: {data[:40]}...")
                print(f"   → Assigned: {result.suggested_name or result.prefix}")
                print()
        except Exception as e:
            print(f"❌ Failed to store: {e}")
            print()
    
    # Query by automatically assigned prefixes
    print("🔍 Querying by automatically assigned prefixes...")
    print()
    
    queries = [
        "ISA_",
        "PATTERN_",
        "LEARNING_",
        "AGENT_123:",
        "DOMAIN_PHYSICS:"
    ]
    
    for prefix in queries:
        results = backend.find_by_prefix(prefix, limit=10)
        if results:
            print(f"✅ Found {len(results)} nodes with prefix '{prefix}'")
            for node in results[:3]:  # Show first 3
                node_data = node.get('data', '')
                if isinstance(node_data, bytes):
                    node_data = node_data.decode('utf-8', errors='ignore')
                print(f"   - {node.get('name', 'unknown')}: {node_data[:40]}...")
        else:
            print(f"⚠️  No nodes found with prefix '{prefix}'")
        print()
    
    backend.close()
    print("✅ Demo complete!")


if __name__ == "__main__":
    try:
        # Demo 1: Classification
        demo_automatic_classification()
        
        # Demo 2: Storage
        demo_automatic_storage()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
