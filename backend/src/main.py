from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import embed, query, scrape

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],    
)

app.include_router(query.router)
app.include_router(scrape.router)
app.include_router(embed.router)
