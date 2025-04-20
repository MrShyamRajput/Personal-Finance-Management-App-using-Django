from pymongo import MongoClient
import bcrypt

# MongoDB Atlas connection URI (replace with your details)
client = MongoClient(
    "mongodb+srv://mr__shyam_rajput:mr__shyam_rajput@mycluster.oxgncag.mongodb.net/?retryWrites=true&w=majority"
)

# Choose your DB and collection
db = client["finance_db"]
users_collection = db["login_data"]

# Check if connected
if db is not None:
    print("Connected successfully to MongoDB Atlas!")
