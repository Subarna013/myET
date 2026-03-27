from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from recommender import get_personalized_feed
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# GET FEED
# -----------------------------
@app.get("/feed/{user_id}")
def get_feed(user_id: int, db: Session = Depends(get_db)):

    # get user interests
    interests = db.query(models.Interest).filter(
        models.Interest.user_id == user_id
    ).all()

    topics = [i.topic for i in interests]

    # get personalized news
    articles = get_personalized_feed(topics)

    return {"articles": articles}

# -----------------------------
# SIGNUP
# -----------------------------
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(
        name=user.name,
        phone=user.phone,
        password=user.password,
        persona=user.persona
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # save interests
    for i in user.interests:
        db.add(models.Interest(user_id=new_user.id, topic=i.lower()))

    db.commit()

    return {"user_id": new_user.id}


# -----------------------------
# LOGIN
# -----------------------------
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.phone == user.phone,
        models.User.password == user.password
    ).first()

    if not db_user:
        return {"error": "Invalid credentials"}

    return {"user_id": db_user.id, "persona": db_user.persona}