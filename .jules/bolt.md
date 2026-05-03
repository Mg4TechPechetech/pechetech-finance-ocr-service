## 2024-05-24 - FastAPI ML Engine Dependency Injection & CPU-Bound Operations
**Learning:** In FastAPI applications integrating ML models (like OCR or NLP engines), instantiating these models per-request blocks the event loop and wastes memory/CPU. Furthermore, executing these CPU-bound tasks in async routes directly blocks concurrent requests.
**Action:** Always cache the instantiation of ML components injected via dependency injection using `@lru_cache()` from `functools`. Always offload the execution of these synchronous CPU-bound models using `await asyncio.to_thread(func)`.
