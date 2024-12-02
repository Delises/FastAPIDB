from fastapi import FastAPI
from api import get_cve, init_db

app = FastAPI()
app.include_router(get_cve.router)
app.include_router(init_db.router)
