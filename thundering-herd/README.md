# Thundering Herd Demo

A small Streamlit app that shows how concurrent requests for the same uncached item can produce duplicate database work.

It compares three approaches:

- **Naive:** every request calls the database.
- **Local coalescing:** concurrent requests are combined within each API instance.
- **Distributed lock:** API instances coordinate through Redis, resulting in one database call.

## Run locally

From this directory, create a virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install streamlit redis
```

The distributed-lock example requires Redis on `localhost:6379`. For example:

```bash
docker run --rm -p 6379:6379 redis
```

Start the UI:

```bash
streamlit run ui.py
```

Choose the number of concurrent requests and simulated API instances, then run each approach to compare its database-call count and elapsed time.
