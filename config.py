import os
from dotenv import load_dotenv

# load variables from .env file
load_dotenv()

#Take my_id from .env file
my_id = int(os.getenv("MYID"))
# Take bot token from .env file
bot_token = os.getenv("TOKEN")

#SERVER_CONNECTION
db_host = os.getenv("db_host")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_name = os.getenv("db_name")