from app.database import Base, engine
from app.models import Department, Employee

def main():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()


