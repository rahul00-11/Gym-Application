from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Literal

from database.data import get_db_connection

router = APIRouter()


# =========================
# USER PROFILE MODEL
# =========================
class UserProfile(BaseModel):

    age: Annotated[
        int,
        Field(
            gt=14,
            lt=80,
            description="User age must be between 15 and 79"
        )
    ]

    height: Annotated[
        float,
        Field(
            gt=50,
            lt=300,
            description="Height in cm"
        )
    ]

    weight: Annotated[
        float,
        Field(
            gt=20,
            lt=500,
            description="Weight in kg"
        )
    ]

    goal: Literal[
        "Muscle Gain",
        "Fat Loss",
        "Maintenance"
    ]

    experience_level: Literal[
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    weekly_change: Annotated[
        float,
        Field(
            ge=-2,
            le=2,
            description="Weight change per week in kg"
        )
    ] = 0.0


# =========================
# CALORIE CALCULATION
# =========================
def calculate_daily_calories(
    age: int,
    height: float,
    weight: float,
    experience_level: str,
    goal: str,
    weekly_change: float = 0.0
):

    # Mifflin-St Jeor Formula
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    # Activity Level
    activity_map = {
        "Beginner": 1.5,
        "Intermediate": 1.55,
        "Advanced": 1.8
    }

    activity_factor = activity_map.get(experience_level, 1.2)

    # Maintenance Calories
    maintenance_calories = bmr * activity_factor

    # Maintenance goal automatically sets weekly_change to 0
    if goal == "Maintenance":
        weekly_change = 0

    # Daily calorie adjustment
    daily_adjustment = (weekly_change * 7700) / 7

    target_calories = maintenance_calories + daily_adjustment

    # Goal text
    if goal == "Muscle Gain":
        weekly_target = f"Gain {weekly_change} kg/week"

    elif goal == "Fat Loss":
        weekly_target = f"Lose {abs(weekly_change)} kg/week"

    else:
        weekly_target = "Maintain current weight"

    return {
        "bmr": round(bmr),
        "maintenance_calories": round(maintenance_calories),
        "target_calories": round(target_calories),
        "weekly_target": weekly_target
    }


# =========================
# SETUP HOME PROFILE
# =========================
@router.post("/home/setup")
def setup_home(profile: UserProfile):

    calorie_data = calculate_daily_calories(
        profile.age,
        profile.height,
        profile.weight,
        profile.experience_level,
        profile.goal,
        profile.weekly_change
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_profile
        (
            age,
            height,
            weight,
            goal,
            experience_level,
            weekly_change
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            profile.age,
            profile.height,
            profile.weight,
            profile.goal,
            profile.experience_level,
            profile.weekly_change
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "Profile saved successfully",
        "calories": calorie_data,
        "profile": profile.model_dump()
    }


# =========================
# GET HOME DATA
# =========================
@router.get("/home")
def get_home():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM user_profile
        ORDER BY id DESC
        LIMIT 1
        """
    )

    profile = cursor.fetchone()

    conn.close()

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="No profile found"
        )

    calorie_data = calculate_daily_calories(
        profile["age"],
        profile["height"],
        profile["weight"],
        profile["experience_level"],
        profile["goal"],
        profile["weekly_change"]
    )

    return {
        "profile": dict(profile),
        "calories": calorie_data
    }