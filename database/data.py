import sqlite3

DB_NAME = "gym_app.db"


# =========================
# DATABASE CONNECTION
# =========================
def get_db_connection():

    conn = sqlite3.connect(DB_NAME)

    # Access rows like dictionary
    conn.row_factory = sqlite3.Row

    return conn


# =========================
# INITIALIZE DATABASE
# =========================
def init_db():

    conn = get_db_connection()

    cursor = conn.cursor()

    # =========================
    # USER PROFILE TABLE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        age INTEGER NOT NULL CHECK(age >= 15),

        height REAL NOT NULL CHECK(height > 0),

        weight REAL NOT NULL CHECK(weight > 0),

        goal TEXT NOT NULL,

        experience_level TEXT NOT NULL,

        weekly_change REAL DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # CALORIES TABLE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calories (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        food_name TEXT NOT NULL,

        calories INTEGER NOT NULL CHECK(calories >= 0),

        protein REAL DEFAULT 0,

        carbs REAL DEFAULT 0,

        fats REAL DEFAULT 0,

        meal_type TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS workouts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    workout_session_id INTEGER,

    muscle_group TEXT NOT NULL,

    exercise_name TEXT NOT NULL,

    set_number INTEGER NOT NULL CHECK(set_number > 0),

    reps INTEGER NOT NULL CHECK(reps > 0),

    weight REAL NOT NULL CHECK(weight >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")

    conn.commit()

    conn.close()

    print("Database initialized successfully")


# =========================
# RUN DATABASE SETUP
# =========================
if __name__ == "__main__":

    init_db()