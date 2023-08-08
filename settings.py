from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES", default=1)
SECRET_KEY = os.getenv("SECRET_KEY", default = "secret_key228")
ALGORITHM = os.getenv("ALGORITHM", default="HS256")