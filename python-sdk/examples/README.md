# Synrix examples

Run from the **repository root** with the engine available: set `SYNRIX_LIB_PATH` (Windows) or `LD_LIBRARY_PATH` (Linux) to the directory containing `libsynrix.dll` / `libsynrix.so`, then:

```bash
pip install -e python-sdk/
python python-sdk/examples/hello_memory.py
```

## Core demos

| Script | Description |
|--------|-------------|
| [hello_memory.py](hello_memory.py) | Local memory, prefix queries |
| [ai_agent_synrix_demo.py](ai_agent_synrix_demo.py) | Multi-session agent memory |
| [test_scale_nodes.py](test_scale_nodes.py) | O(k) scaling (e.g. 100K nodes) |
| [benchmark_synrix.py](benchmark_synrix.py) | Latency/throughput benchmark |
| [reasoning_chain_benchmark.py](reasoning_chain_benchmark.py) | 18-query reasoning chain (Synrix vs simulated backends) |

## Robotics

| Script | Description |
|--------|-------------|
| [robotics_quick_demo.py](robotics_quick_demo.py) | RoboticsNexus: sensors, state, actions |

Use the `synrix.robotics.RoboticsNexus` module for persistent robotics memory.

## RAG examples

These require the **synrix_rag** package (separate install, e.g. from synrix-rag-sdk):

| Script | Description |
|--------|-------------|
| [rag_simple_demo.py](rag_simple_demo.py) | Minimal RAG: ingest, search, context |
| [rag_demo.py](rag_demo.py) | Document ingestion and semantic search |
| [rag_demo_kb.py](rag_demo_kb.py) | Knowledge-base style (support/docs corpus) |

See the main [python-sdk README](../README.md) for installation and engine setup.
