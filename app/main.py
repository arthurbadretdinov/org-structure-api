from fastapi import FastAPI
import uvicorn

from app.router import router
from app.database import Base, engine
from app.models import Department, Employee

app = FastAPI()
app.include_router(router)

def main():
    Base.metadata.create_all(bind=engine)
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()


