from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Literal

from database.data import get_db_connection

router = APIRouter()


# =========================
# CALORIE MODEL
# =========================
class CalorieLog(BaseModel):

    food_name: str

    calories: Annotated[
        int,
        Field(
            ge=0,
            description="Calories amount"
        )
    ]

    protein: Annotated[
        float,
        Field(
            ge=0
        )
    ] = 0

    carbs: Annotated[
        float,
        Field(
            ge=0
        )
    ] = 0

    fats: Annotated[
        float,
        Field(
            ge=0
        )
    ] = 0

    meal_type: Literal[
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snack"
    ]


# =========================
# ADD CALORIE LOG
# =========================
@router.post("/calories/add")
def add_calories(log: CalorieLog):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO calories
        (
            food_name,
            calories,
            protein,
            carbs,
            fats,
            meal_type
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            log.food_name,
            log.calories,
            log.protein,
            log.carbs,
            log.fats,
            log.meal_type
        )
    )

    conn.commit()

    conn.close()

    return {
        "message": "Calories logged successfully",
        "data": log.model_dump()
    }


# =========================
# GET ALL CALORIES
# =========================
@router.get("/calories")
def get_calories():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM calories
    ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return {
        "total_logs": len(logs),
        "logs": [dict(log) for log in logs]
    }


# =========================
# DAILY CALORIE SUMMARY
# =========================
@router.get("/calories/summary")
def calorie_summary():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        SUM(calories) as total_calories,
        SUM(protein) as total_protein,
        SUM(carbs) as total_carbs,
        SUM(fats) as total_fats
    FROM calories
    """)

    summary = cursor.fetchone()

    conn.close()

    return {
        "total_calories": summary["total_calories"] or 0,
        "total_protein": summary["total_protein"] or 0,
        "total_carbs": summary["total_carbs"] or 0,
        "total_fats": summary["total_fats"] or 0
    }