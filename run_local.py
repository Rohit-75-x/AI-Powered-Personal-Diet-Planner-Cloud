"""
One-Click Local Launcher & Demo Seeder
Script: run_local.py
Purpose: Sets up initial demo user (demo@cloudhealth.org / DemoPass123),
         pre-populates demo meal plans, verifies environment, and starts the server.
"""

import sys
import os
import webbrowser
import threading
import time

# Ensure project root in python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from cloud.database_service import get_database
from cloud.storage_service import get_storage
from backend.services.auth_service import AuthService
from backend.app import run_server


def seed_demo_data():
    db = get_database()
    storage = get_storage()

    demo_email = "demo@cloudhealth.org"
    existing_user = db.get_user_by_email(demo_email)

    if not existing_user:
        print("[+] Seeding default demo student account...")
        pwd_hash = AuthService.hash_password("DemoPass123")
        demo_user = db.create_user({
            "name": "Alex Morgan (Demo User)",
            "email": demo_email,
            "password_hash": pwd_hash
        })
        user_id = demo_user["user_id"]

        # Seed profile
        db.save_profile(user_id, {
            "age": 23,
            "gender": "male",
            "height_cm": 178,
            "weight_kg": 72,
            "activity_level": "moderate",
            "dietary_preference": "vegetarian",
            "goal": "weight_loss",
            "allergies": "peanuts",
            "bmr": 1712.5,
            "tdee": 2654.4,
            "target_calories": 2176
        })

        # Seed initial sample plan
        mock_plan = {
            "source_engine": "Rule-Based Heuristic Knapsack Engine",
            "goal": "Weight Loss / Caloric Deficit",
            "dietary_preference": "vegetarian",
            "target_calories": 2176,
            "planned_calories": 2140,
            "meals": {
                "breakfast": {
                    "meal_name": "Rolled Oats with Berries & Sliced Almonds",
                    "description": "Slow-cooked rolled oats with blueberries, chia seeds, and plant milk.",
                    "calories": 320, "protein_g": 12, "carbs_g": 54, "fat_g": 6, "fiber_g": 8,
                    "prep_time_min": 10, "cuisine": "Continental"
                },
                "lunch": {
                    "meal_name": "Yellow Moong Dal with Spinach & Brown Basmati",
                    "description": "Tempered yellow lentils cooked with organic spinach, served with brown basmati rice.",
                    "calories": 460, "protein_g": 20, "carbs_g": 72, "fat_g": 8, "fiber_g": 10,
                    "prep_time_min": 25, "cuisine": "Indian"
                },
                "snack": {
                    "meal_name": "Tangy Mixed Moong Sprouts Chaat",
                    "description": "Sprouted mung beans with onions, tomatoes, lemon juice, and chaat masala.",
                    "calories": 160, "protein_g": 10, "carbs_g": 26, "fat_g": 2, "fiber_g": 7,
                    "prep_time_min": 8, "cuisine": "Indian"
                },
                "dinner": {
                    "meal_name": "Home-style Palak Paneer with Cumin Fragrant Rice",
                    "description": "Cottage cheese cubes simmered in spiced pureed spinach gravy with jeera rice.",
                    "calories": 480, "protein_g": 24, "carbs_g": 46, "fat_g": 22, "fiber_g": 7,
                    "prep_time_min": 25, "cuisine": "Indian"
                }
            },
            "nutrition_summary": {
                "total_calories": 2140,
                "total_protein_g": 146,
                "total_carbs_g": 218,
                "total_fat_g": 68,
                "total_fiber_g": 32,
                "calorie_variance": -36
            },
            "hydration_guideline": "Drink at least 2.8 to 3.2 Liters of water throughout the day.",
            "disclaimer": "Educational wellness simulation. Not clinical medical advice."
        }
        saved_plan = db.save_diet_plan(user_id, mock_plan)

        # Seed sample exported file into Cloud Object Storage
        stored_file = storage.export_plan_as_file(user_id, saved_plan, export_format="txt")
        db.record_file_metadata(user_id, stored_file)

        print(f"[✓] Demo account created: {demo_email} | Password: DemoPass123")
    else:
        print("[✓] Demo account already initialized.")


def open_browser_delayed(url: str, delay: float = 1.5):
    time.sleep(delay)
    try:
        webbrowser.open(url)
    except Exception:
        pass


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print("\n[+] Initializing Cloud Environment & Local Databases...")
    seed_demo_data()
    
    url = f"http://localhost:{port}"
    threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()
    run_server(port=port)
