
import asyncio

db_calls = 0

async def fetch_from_db(product_id: int):
    global db_calls
    
    db_calls += 1
    print(f"DB call count: {db_calls} for product_id: {product_id}")
    
    # Simulate a database call with asyncio.sleep
    await asyncio.sleep(0.4)
    
    return {"id": product_id, 
            "name": "laptop",
            "price": 1000.00
            }
    
cache = {}
in_flight = {
    instance_id: {}
    for instance_id in range(20)
}


# Simulating 20 different API servers, each with its own in-flight requests dictionary.
async def get_product(instance_id: int, product_id: int):

    if product_id in cache:
        return cache[product_id]

    instance_in_flight = in_flight[instance_id]

    if product_id in instance_in_flight:
        return await instance_in_flight[product_id]

    task = asyncio.create_task(fetch_from_db(product_id))
    instance_in_flight[product_id] = task

    try:
        product = await task
        cache[product_id] = product
        return product
    finally:
        del instance_in_flight[product_id]




async def main():

    requests = [
        get_product(i % 20, 42)
        for i in range(100)
    ]

    await asyncio.gather(*requests)

    print()
    print("Requests: 100")
    print(f"Database calls: {db_calls}")
    
asyncio.run(main())
    