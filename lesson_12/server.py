import abc
import random
import string
import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

API_KEY = os.getenv("ALPHAVANTAGE_KEY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def random_string(n: int) -> str:
    return "".join((random.choice(string.ascii_letters) for _ in range(n)))


class GenerationService(abc.ABC):
    @abc.abstractmethod
    async def generate_random_article_idea(self) -> dict:
        pass

    @abc.abstractmethod
    async def generate_technical_guide(self) -> dict:
        pass

    @abc.abstractmethod
    async def generate_fiction(self) -> dict:
        pass


class ArticleGenerationService(GenerationService):
    async def generate_random_article_idea(self) -> dict:
        return {
            "title": random_string(10),
            "idea": random_string(300),
        }

    async def _generate_content(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [
                        {"parts": [
                            {"text": prompt}
                        ]}
                    ]
                },
            )
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text",
                                                                                            "No response from Gemini.").strip()

    async def generate_technical_guide(self) -> dict:
        prompt = "Generate a technical guide on using Gemini"
        idea = await self._generate_content(prompt)
        return {
            "title": "Technical guide on using Gemini",
            "idea": idea,
        }

    async def generate_fiction(self) -> dict:
        prompt = "Generate a story about the future of planet Earth without wars and diseases"
        idea = await self._generate_content(prompt)
        return {
            "title": "Story about the future of planet Earth",
            "idea": idea,
        }


article_service = ArticleGenerationService()


async def get_exchange_rate() -> str:
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=CURRENCY_EXCHANGE_RATE&from_currency=UAH&to_currency=USD&apikey={API_KEY}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = await response.json()
        return data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

@app.get("/fetch-market")
async def fetch_market():

    """
       User Request:           None
       User Response:          str

       Alphavantage Request:   dict
       Alphavantage Response:  dict
       {'Realtime Currency Exchange Rate': {'1. From_Currency Code': 'UAH',
                '2. From_Currency Name': 'Ukrainian '
                                         'Hryvnia',
                '3. To_Currency Code': 'USD',
                '4. To_Currency Name': 'United States '
                                       'Dollar',
                '5. Exchange Rate': '0.02380000',
                '6. Last Refreshed': '2025-01-06 19:37:43',
                '7. Time Zone': 'UTC',
                '8. Bid Price': '0.02379000',
                '9. Ask Price': '0.02380000'}
       }
       """

    rate = await get_exchange_rate()
    return {"rate": rate}

@app.get("/article-idea")
async def article_idea():
    return await article_service.generate_random_article_idea()


@app.get("/story-fiction")
async def story_fiction():
    return await article_service.generate_fiction()


@app.get("/technical-guide")
async def technical_guide():
    return await article_service.generate_technical_guide()

