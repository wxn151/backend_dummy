import os

#from dotenv import load_dotenv
#load_dotenv()

## system
title = os.getenv("TITLE")
description = os.getenv("DESCRIPTION")

# conn
DATABASE_URL = os.getenv("DATABASE_URL")

# hash
SECRET_KEY = os.getenv("SECRET_KEY")

# credentials SMTP
MAIL = os.getenv("MAIL")
PASSWORD = os.getenv("PASSWORD")

# encrytion ALGORITHM
ALGORITHM = os.getenv("ALGORITHM")

# reset link base
RESET = os.getenv("RESET_LINK")
ACTIVATE = os.getenv("ACTIVATE_LINK")
