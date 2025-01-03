import asyncio
import random
import httpx
import time
import argparse
import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

async def ahttp_request(url: str) -> str:
    print(f"requesting {url}")
    response: requests.Response = await asyncio.to_thread(requests.get, url)

    return response.json()["name"]


async def http_request(url: str) -> str:
    print(f"Requesting {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()["name"]


def get_urls(n: int) -> list[str]:
    return [BASE_URL.format(pokemon_id=random.randint(1, 500)) for _ in range(n)]


async def async_pokemons_httpx():
    urls: list[str] = get_urls(n=50)
    tasks = [http_request(url) for url in urls]
    results = await asyncio.gather(*tasks)

    return results


async def async_pokemons_request():
    urls: list[str] = get_urls(n=50)
    tasks = [ahttp_request(url) for url in urls]
    results = await asyncio.gather(*tasks)

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "library",
        choices=["httpx", "requests"],
        default="httpx",
        nargs="?"
    )
    args = parser.parse_args()

    start = time.perf_counter()

    if args.library == "httpx":
        data = asyncio.run(async_pokemons_httpx())
    elif args.library == "requests":
        data = asyncio.run(async_pokemons_request())

    end = time.perf_counter()

    print(data)
    print(f"the len of the collection: {len(data)}")
    print(f"execution time: {end - start}")


if __name__ == "__main__":
    raise SystemExit(main())
