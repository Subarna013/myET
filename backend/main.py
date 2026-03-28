from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from recommender import get_personalized_feed
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# CREATE TABLES
# -----------------------------
models.Base.metadata.create_all(bind=engine)

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI()

# ✅ CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# DB DEPENDENCY
# -----------------------------
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

    interests = db.query(models.Interest).filter(
        models.Interest.user_id == user_id
    ).all()

    topics = [i.topic for i in interests]

    articles = get_personalized_feed(topics)

    return {"articles": articles}


# -----------------------------
# SIGNUP (FIXED)
# -----------------------------
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        # create user
        new_user = models.User(
            name=user.name,
            phone=user.phone,
            password=user.password,
            persona=user.persona
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # ✅ SAFE INTEREST INSERT
        if user.interests:
            for i in user.interests:
                if i and isinstance(i, str):  # avoid empty / bad values
                    db.add(models.Interest(
                        user_id=new_user.id,
                        topic=i.lower().strip()
                    ))

        db.commit()

        return {"user_id": new_user.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


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
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "user_id": db_user.id,
        "persona": db_user.persona
    }
