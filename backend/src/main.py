from fastapi import FastAPI
from routers import embed, query, scrape

app = FastAPI()

app.include_router(query.router)
app.include_router(scrape.router)
app.include_router(embed.router)
