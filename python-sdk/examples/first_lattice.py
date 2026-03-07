#!/usr/bin/env python3
"""
Your First Lattice - Guided Tutorial

A step-by-step tutorial for building your first lattice with SYNRIX.
Perfect for beginners - no prior experience needed!

This tutorial will teach you:
1. What a lattice is (in simple terms)
2. How to create nodes (pieces of knowledge)
3. How to connect related concepts
4. How to query your lattice
5. How to build something useful

Let's build a lattice about programming concepts!

INSTALLATION:
  First, install the SDK:
    cd python-sdk
    pip install -e .

  Then run this tutorial:
    python examples/first_lattice.py
"""

try:
    from synrix import SynrixMockClient
except ImportError:
    import sys
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from synrix import SynrixMockClient
    except ImportError:
        print("=" * 60)
        print("SYNRIX SDK not found!")
        print("=" * 60)
        print("\nPlease install the SDK first:")
        print("\n  pip install -e .")
        print("\nOr from PyPI:")
        print("\n  pip install synrix")
        print("\nThen run:")
        print("  python examples/first_lattice.py")
        sys.exit(1)

import time


def print_step(step_num, title):
    print("\n" + "=" * 60)
    print(f"STEP {step_num}: {title}")
    print("=" * 60)
    time.sleep(0.5)


def print_info(text):
    print(f"\n{text}")
    time.sleep(0.3)


def print_success(text):
    print(f"OK: {text}")
    time.sleep(0.2)


def wait_for_user():
    input("\nPress Enter to continue... ")


def main():
    print("""
========================================================
  Your First Lattice - Guided Tutorial
  Learn to build a lattice in 5 simple steps!
========================================================
    """)

    print_info("What is a lattice?")
    print("""
A lattice is a flat, high-speed store where:
  - Each piece of information is a node (a fact, concept, or data blob)
  - Nodes are addressed by semantic prefixes for O(k) retrieval
  - You can query the lattice instantly regardless of how many nodes it holds

Think of it as a purpose-built memory plane for AI agents:
structured, fast, and crash-safe.
    """)

    wait_for_user()

    # Initialize client
    print_step(1, "Setting Up Your Lattice")
    print("\nFirst, let's create a SYNRIX client...")
    client = SynrixMockClient()
    print_success("Client created!")

    print_info("We're using the mock client, which means:")
    print("  - No server needed - everything runs in memory")
    print("  - Perfect for learning and testing")
    print("  - Same API as the real SYNRIX engine")

    print("\nNow let's create a collection to hold our nodes:")
    collection_name = "programming_concepts"
    client.create_collection(collection_name)
    print_success(f"Collection '{collection_name}' created!")

    wait_for_user()

    # Add nodes
    print_step(2, "Adding Your First Nodes")
    print("\nNodes are the building blocks of your lattice.")
    print("Each node represents a concept, fact, or piece of information.")

    print("\nLet's add some programming concepts:")
    concepts = [
        ("PROGRAMMING_LANGUAGE:Python",     "Python is a high-level programming language known for its simplicity"),
        ("PROGRAMMING_LANGUAGE:JavaScript", "JavaScript is a programming language used for web development"),
        ("CONCEPT:Variable",                "A variable is a container that stores a value"),
        ("CONCEPT:Function",                "A function is a reusable block of code that performs a specific task"),
        ("CONCEPT:Class",                   "A class is a blueprint for creating objects"),
    ]

    node_ids = []
    for name, description in concepts:
        node_id = client.add_node(name, description, collection=collection_name)
        node_ids.append((node_id, name))
        print(f"  Added: {name}")
        print(f"     {description[:60]}...")
        time.sleep(0.2)

    print_success(f"Added {len(concepts)} nodes to your lattice!")

    print_info("Notice the naming pattern:")
    print("  - PROGRAMMING_LANGUAGE:Python")
    print("  - CONCEPT:Variable")
    print("\nThis prefix pattern helps us organize and query related nodes")
    print("together with O(k) performance - speed depends on result count,")
    print("not total lattice size.")

    wait_for_user()

    # Query
    print_step(3, "Querying Your Lattice")
    print("\nNow let's search for nodes by their prefix:")

    print("\nSearching for all programming languages...")
    languages = client.query_prefix("PROGRAMMING_LANGUAGE:", collection=collection_name)
    print_success(f"Found {len(languages)} programming languages:")
    for result in languages:
        name = result.get("payload", {}).get("name", "unknown")
        data = result.get("payload", {}).get("data", "")
        print(f"  - {name.replace('PROGRAMMING_LANGUAGE:', '')}: {data[:50]}...")

    print("\nSearching for all concepts...")
    concepts_found = client.query_prefix("CONCEPT:", collection=collection_name)
    print_success(f"Found {len(concepts_found)} concepts:")
    for result in concepts_found:
        name = result.get("payload", {}).get("name", "unknown")
        data = result.get("payload", {}).get("data", "")
        print(f"  - {name.replace('CONCEPT:', '')}: {data[:50]}...")

    print_info("This is the power of prefix queries:")
    print("  - Fast retrieval of related concepts")
    print("  - Organized by category automatically")
    print("  - Scales to millions of nodes with no performance cliff")

    wait_for_user()

    # Expand
    print_step(4, "Expanding Your Lattice")
    print("\nLet's add more nodes:")

    more_concepts = [
        ("CONCEPT:List",                  "A list is an ordered collection of items"),
        ("CONCEPT:Dictionary",            "A dictionary stores key-value pairs"),
        ("CONCEPT:Loop",                  "A loop repeats code until a condition is met"),
        ("PROGRAMMING_LANGUAGE:Java",     "Java is an object-oriented programming language"),
        ("PROGRAMMING_LANGUAGE:C++",      "C++ is a general-purpose programming language"),
    ]

    for name, description in more_concepts:
        client.add_node(name, description, collection=collection_name)
        print(f"  Added: {name}")
        time.sleep(0.1)

    print_success(f"Added {len(more_concepts)} more nodes!")

    print("\nYour lattice now contains:")
    languages = client.query_prefix("PROGRAMMING_LANGUAGE:", collection=collection_name)
    concepts  = client.query_prefix("CONCEPT:", collection=collection_name)
    print(f"  - {len(languages)} programming languages")
    print(f"  - {len(concepts)} programming concepts")

    wait_for_user()

    # Real-world use
    print_step(5, "Building Something Useful")
    print("\nLet's build a simple 'programming tutor' that can answer questions!")

    print("\nExample: 'What programming languages do you know about?'")
    languages = client.query_prefix("PROGRAMMING_LANGUAGE:", collection=collection_name)
    print("\nAnswer:")
    for result in languages:
        name = result.get("payload", {}).get("name", "unknown")
        print(f"  - {name.replace('PROGRAMMING_LANGUAGE:', '')}")

    print("\nExample: 'What is a variable?'")
    variables = client.query_prefix("CONCEPT:Variable", collection=collection_name)
    if variables:
        answer = variables[0].get("payload", {}).get("data", "")
        print(f"\nAnswer: {answer}")

    print_info("This is how a lattice powers AI systems:")
    print("  - Store structured knowledge as nodes")
    print("  - Query instantly for relevant information")
    print("  - Use in RAG (Retrieval-Augmented Generation) pipelines")
    print("  - Back long-running agents with persistent, crash-safe memory")

    wait_for_user()

    # Summary
    print("\n" + "=" * 60)
    print("CONGRATULATIONS!")
    print("=" * 60)
    print("\nYou've built your first lattice!")

    print("\nWhat you learned:")
    print("  - What a lattice is")
    print("  - How to create nodes")
    print("  - How to organize nodes with semantic prefixes")
    print("  - How to query your lattice with O(k) prefix search")
    print("  - How a lattice powers AI memory and retrieval")

    print("\nNext steps:")
    print("  1. Add more nodes to your lattice")
    print("  2. Try different prefix patterns")
    print("  3. Build a simple Q&A system")
    print("  4. Switch to RawSynrixBackend for direct C engine access")
    print("  5. Integrate with an LLM for RAG")

    print("\nTips:")
    print("  - Use consistent prefix patterns (CATEGORY:Item)")
    print("  - Keep node data clear and concise")
    print("  - Organize related concepts under the same prefix")
    print("  - Use add_node_deduplicated() to avoid storing duplicate content")

    print("\nResources:")
    print("  - examples/quickstart.py for a faster intro")
    print("  - Read README.md for full API documentation")

    print("\n" + "=" * 60)
    print("Happy lattice building!")
    print("=" * 60 + "\n")

    client.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTutorial interrupted. Come back anytime!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Don't worry - this is just a tutorial. Try running it again!")
