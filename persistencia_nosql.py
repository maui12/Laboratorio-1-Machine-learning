from pymongo import MongoClient
from datetime import datetime, timezone

def guardar_en_mongodb(df, mongo_uri, db_name, coll_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[coll_name]
    
    for _, row in df.iterrows():
        documento = row.to_dict()
        documento["_id"] = f"{row['fuente']}::{row['id']}"
        collection.update_one(
            {"_id": documento["_id"]},
            {"$set": documento},
            upsert=True
        )