from typing import List

from pymongo import AsyncMongoClient

from config import *



class MongoDB:
    def __init__(self) -> None:
        self.mongo = AsyncMongoClient(config.MONGO_DB_URI)
        self.db = self.mongo.Star
        self.nks = self.db.nokos

    async def add_nokos(
        self,
        _id: int = None,
        price: str = None,
        session: str = None,
        phone: str = None,
        otp: str = None,
        twofa: str = None,
        user_id: int = None,
        session_string: str = None,
    ):
        nokos_id = _id or user_id

        if not nokos_id:
            raise ValueError("_id atau user_id wajib diisi")

        old_data = await self.get_nokos_by_id(nokos_id)

        update_data = {}

        if price is not None:
            update_data["price"] = str(price)
        elif old_data and old_data.get("price") is not None:
            update_data["price"] = str(old_data.get("price"))
        else:
            update_data["price"] = "0"

        if session_string is not None:
            update_data["session"] = session_string
        elif session is not None:
            update_data["session"] = session
        elif old_data and old_data.get("session") is not None:
            update_data["session"] = old_data.get("session")
        else:
            update_data["session"] = ""

        if phone is not None:
            update_data["phone"] = phone

        if otp is not None:
            update_data["otp"] = otp

        if twofa is not None:
            update_data["twofa"] = twofa

        return await self.nks.update_one(
            {"_id": int(nokos_id)},
            {"$set": update_data},
            upsert=True,
        )

    async def delete_nokos(self, _id: int):
        return await self.nks.delete_one({"_id": int(_id)})

    async def get_nokos(self):
        result = []
        cursor = self.nks.find({"_id": {"$exists": True}})
        async for data in cursor:
            result.append(data)
        return result

    async def get_nokos_by_id(self, _id: int):
        return await self.nks.find_one({"_id": int(_id)})


db = MongoDB()