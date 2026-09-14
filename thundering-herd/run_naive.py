import asyncio
from time import perf_counter


async def run_naive(requests: int = 100, instances: int = 20):
    """Run a fresh cold-cache simulation across the requested API instances."""
    if requests < 1 or instances < 1:
        raise ValueError("Requests and instances must be positive")

    db_calls = 0
    cache = {}
    inflight = [{} for _ in range(instances)]

    async def fetch_from_db(product_id):
        nonlocal db_calls
        db_calls += 1
        await asyncio.sleep(0.4)
        return {"id": product_id, "name": "laptop", "price": 1000.00}

    async def get_product(instance_id, product_id):
        if product_id in cache:
            return cache[product_id]
        product = await fetch_from_db(product_id)
        cache[product_id] = product
        return product

    started = perf_counter()
    await asyncio.gather(*(get_product(i % instances, 42) for i in range(requests)))
    return {
        "requests": requests,
        "db_calls": db_calls,
        "elapsed_ms": (perf_counter() - started) * 1000,
    }


if __name__ == "__main__":
    print(asyncio.run(run_naive()))
