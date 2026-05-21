from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.data import init_db

from router.home import router as home_router
from router.workout import router as workout_router
from router.caloires import router as caloire_router


# =========================
# INITIALIZE FASTAPI APP
# =========================
app = FastAPI(
    title="Gym Application Backend",
    description="AI-powered gym app with profile setup, calorie calculator, and workout logging",
    version="1.0.0"
)


# =========================
# ENABLE CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# INITIALIZE DATABASE
# =========================
init_db()


# =========================
# INCLUDE ROUTERS
# =========================
app.include_router(
    home_router,
    prefix="",
    tags=["Home"]
)

app.include_router(
    workout_router,
    prefix="",
    tags=["Workouts"]
)

app.include_router(
    caloire_router,
    prefix="",
    tags=["Calories"]
)


# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def root():

    return {
        "message": "Welcome to the Gym Application API"
    }