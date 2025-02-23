import os
from dotenv import load_dotenv
from bot import app

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("Bot starting...")
    app.run()
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​