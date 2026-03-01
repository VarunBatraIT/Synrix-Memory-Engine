#!/usr/bin/env python3
"""
SYNRIX RAG Demo – document ingestion and semantic search.

- Storing documents larger than 512 bytes (Synrix chunked storage)
- Semantic search and context retrieval for LLM-style RAG

Requires: synrix_rag package. Run with SYNRIX_LIB_PATH set:
  cd python-sdk && pip install -e . && python examples/rag_demo.py
"""

import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
_sdk_root = os.path.dirname(_script_dir)
if _sdk_root not in sys.path:
    sys.path.insert(0, _sdk_root)


def main():
    demo_lattice = os.path.join(_script_dir, "demo_rag.lattice")
    if os.path.exists(demo_lattice):
        try:
            os.remove(demo_lattice)
        except Exception:
            pass
    print("SYNRIX RAG Demo")
    print("===============\n")

    synrix_client = None
    try:
        from synrix.ai_memory import AIMemory
        synrix_client = AIMemory(lattice_path=demo_lattice)
        print("[OK] Using SYNRIX backend (documents persist, chunked storage for large payloads).\n")
    except ImportError:
        print("[WARN] synrix not installed. Provide SYNRIX DLL for full demo. Using in-memory fallback.\n")
    except Exception as e:
        print(f"[WARN] SYNRIX init failed: {e}\n       Using in-memory fallback.\n")

    from synrix_rag import RAGMemory

    rag = RAGMemory(
        collection_name="synrix_rag_demo",
        embedding_model="local",
        synrix_client=synrix_client,
    )

    docs = [
        {
            "text": (
                "Synrix is a high-performance memory engine designed for AI agents and robotics. "
                "It uses a fixed 512-byte node architecture for speed, with chunked storage for larger payloads. "
                "This document is intentionally long to demonstrate that RAG works with documents exceeding "
                "the single-node limit: the SDK stores them automatically using chunked storage."
            ),
            "metadata": {"source": "synrix_overview", "topic": "architecture"},
        },
        {
            "text": (
                "To build RAG with Synrix you install the SDK and set SYNRIX_LIB_PATH. "
                "Create a RAGMemory instance, add documents with add_document, "
                "use search() for semantic retrieval and get_context() for your LLM."
            ),
            "metadata": {"source": "setup_guide", "topic": "rag"},
        },
    ]

    print("1. Ingesting documents...")
    for i, doc in enumerate(docs):
        doc_id = rag.add_document(text=doc["text"], metadata=doc.get("metadata", {}))
        size = len(doc["text"].encode("utf-8"))
        note = " (chunked)" if size > 511 else ""
        print(f"   Added doc {i+1}: id={doc_id[:8] if doc_id else '?'}... size={size} bytes{note}")
    print()

    print("2. Semantic search: 'How do I set up RAG with Synrix?'")
    results = rag.search("How do I set up RAG with Synrix?", top_k=3)
    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        text_preview = (r.get("text", "") or "")[:120].replace("\n", " ")
        print(f"   [{i}] score={score:.4f} | {text_preview}...")
    print()

    print("3. Get context for LLM (top 2):")
    context = rag.get_context("How do I set up RAG with Synrix?", top_k=2)
    print(context[:500] + "..." if len(context) > 500 else context)
    print("\nDemo complete.")
    if synrix_client and os.path.exists(demo_lattice):
        print(f"Lattice: {demo_lattice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
