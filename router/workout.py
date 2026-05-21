from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

from database.data import get_db_connection

router = APIRouter()


class WorkoutEntry(BaseModel):

    muscle_group: Annotated[
        str,
        Field(min_length=2, max_length=50)
    ]

    exercise_name: Annotated[
        str,
        Field(min_length=2, max_length=100)
    ]

    set_number: Annotated[
        int,
        Field(gt=0, le=20)
    ]

    reps: Annotated[
        int,
        Field(gt=0, le=100)
    ]

    weight: Annotated[
        float,
        Field(ge=0, le=500)
    ]


# CREATE → Add workout entry
@router.post("/workouts")
def add_workout(entry: WorkoutEntry):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO workouts
        (muscle_group, exercise_name, set_number, reps, weight)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            entry.muscle_group,
            entry.exercise_name,
            entry.set_number,
            entry.reps,
            entry.weight
        )
    )

    conn.commit()

    workout_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Workout added successfully",
        "workout_id": workout_id
    }


# READ → Get all workouts
@router.get("/workouts")
def get_workouts():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM workouts ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# UPDATE → Modify workout entry
@router.put("/workouts/{id}")
def update_workout(id: int, entry: WorkoutEntry):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE workouts
        SET muscle_group=?,
            exercise_name=?,
            set_number=?,
            reps=?,
            weight=?
        WHERE id=?
        """,
        (
            entry.muscle_group,
            entry.exercise_name,
            entry.set_number,
            entry.reps,
            entry.weight,
            id
        )
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    conn.close()

    return {
        "message": f"Workout {id} updated successfully"
    }


# DELETE → Remove workout entry
@router.delete("/workouts/{id}")
def delete_workout(id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM workouts WHERE id=?",
        (id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    conn.close()

    return {
        "message": f"Workout {id} deleted successfully"
    }