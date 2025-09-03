from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from core.models import Base
from core.db_helper import db_helper
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_helper.engine.dispose()

app = FastAPI(lifespan=lifespan)

# app.include_router(router=users_router, prefix=settings.api_v1_prefix)
# app.include_router(router=sessions_router, prefix=settings.api_v1_prefix)
# app.include_router(router=topics_router, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
products = [{'name': 'Laptop', 'price': 1000}, {'name': 'Mouse', 'price': 50}, {'name': 'Keyboard', 'price': 120}]
product = products.sort()