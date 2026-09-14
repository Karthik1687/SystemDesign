import asyncio
from time import perf_counter
from uuid import uuid4


async def run_distributed(requests: int = 100, instances: int = 20):
    """Coalesce locally and coordinate simulated instances through Redis."""
    from redis.asyncio import Redis

    if requests < 1 or instances < 1:
        raise ValueError("Requests and instances must be positive")

    redis = Redis(host="localhost", port=6379, decode_responses=True,
                  socket_connect_timeout=5, socket_timeout=5)
    # Each run owns its keys and client, including across Streamlit event loops.
    prefix = f"herd-demo:{uuid4().hex}"
    cache_key = f"{prefix}:product:42"
    lock_key = f"{prefix}:lock:42"
    inflight = [{} for _ in range(instances)]
    db_calls = 0

    async def load_product():
        nonlocal db_calls
        product = await redis.get(cache_key)
        if product is not None:
            return product
        async with redis.lock(lock_key, timeout=5, blocking_timeout=10):
            product = await redis.get(cache_key)
            if product is not None:
                return product
            db_calls += 1
            await asyncio.sleep(0.4)
            product = "product-42"
            await redis.set(cache_key, product, ex=20)
            return product

    async def get_product(instance_id):
        pending = inflight[instance_id]
        if 42 in pending:
            return await pending[42]
        task = asyncio.create_task(load_product())
        pending[42] = task
        try:
            return await task
        finally:
            pending.pop(42, None)

    started = perf_counter()
    tasks = []
    try:
        await redis.ping()
        tasks = [asyncio.create_task(get_product(i % instances)) for i in range(requests)]
        await asyncio.gather(*tasks)
        await redis.delete(cache_key)
        return {
            "requests": requests,
            "db_calls": db_calls,
            "elapsed_ms": (perf_counter() - started) * 1000,
        }
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        await redis.aclose()


if __name__ == "__main__":
    print(asyncio.run(run_distributed()))
