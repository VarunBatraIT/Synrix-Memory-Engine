#!/usr/bin/env python3
"""
SYNRIX Init Example

Demonstrates the new synrix.init() workflow.
"""

import synrix

# Initialize SYNRIX - checks for engine
print("Initializing SYNRIX...")
if synrix.init():
    print("✅ SYNRIX engine found!")
    
    # Now you can use SYNRIX
    client = synrix.SynrixClient(host="localhost", port=6334)
    print("✅ Connected to SYNRIX server")
    
    # Use the client...
    collections = client.get_collections()
    print(f"Found {len(collections.get('result', {}).get('collections', []))} collections")
else:
    print("\nTo install the engine, run:")
    print("  synrix install-engine")
