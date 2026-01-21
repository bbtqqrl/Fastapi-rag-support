# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# import uvicorn

# from core.models import Base
# from core.db_helper import db_helper
# from core.config import settings

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with db_helper.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     await db_helper.engine.dispose()

# app = FastAPI(lifespan=lifespan)

# # app.include_router(router=users_router, prefix=settings.api_v1_prefix)
# # app.include_router(router=sessions_router, prefix=settings.api_v1_prefix)
# # app.include_router(router=topics_router, prefix=settings.api_v1_prefix)

# if __name__ == '__main__':
#     uvicorn.run("main:app", reload=True)

import asyncio
from pathlib import Path
from core.db_helper import db_helper
from core.models.documents import Document
from core.rag.service import ingest_file
from core.rag.service import retrieve_context


async def _manual_test():
    async with db_helper.session_factory() as db:
        file_path = Path('Document 1.pdf')
        file_bytes = file_path.read_bytes()

        document = Document(name=file_path.name, path=str(file_path.resolve()))
        db.add(document)
        await db.commit()
        await db.refresh(document)

        await ingest_file(
            db=db,
            filename=file_path.name,
            file_bytes=file_bytes,
            document_id=document.id,
        )

        print("✅ DONE")
        print("document_id:", document.id)

async def _manual_user_query_test(query: str):
    async with db_helper.session_factory() as db:
        context_chunks = await retrieve_context(db, query, limit=3)
        print("Context Chunks:")
        for i, chunk in enumerate(context_chunks, 1):
            print(f"{i}. {chunk}\n")

if __name__ == "__main__":
    asyncio.run(_manual_user_query_test('Привіт, а як з вами звязатись?'))