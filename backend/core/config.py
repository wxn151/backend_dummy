import os
# from dotenv import load_dotenv

# load_dotenv()

title = "Back end con FastAPI"
description = "Documentación de API"

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql://postgres:Donut.238@localhost:5432/foreign"
# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = "game_boy_advance_2001"

# credentials SMTP
MAIL = "behemothsystem@gmail.com"
PASSWORD = "nrub ezre zibj iklm "

# encrytion ALGORITHM
ALGORITHM = "HS256"

# reset link base
RESET = "http://localhost:5173/reset-password/"
ACTIVATE = "http://localhost:5173/confirm-email/"
