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
        session: str = "",
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

        if price is None and old_data:
            price = old_data.get("price", "0")

        if price is None:
            price = "0"

        if session_string is not None:
            session = session_string

        return await self.nks.update_one(
            {"_id": int(nokos_id)},
            {
                "$set": {
                    "price": str(price),
                    "session": session or "",
                    "phone": phone,
                    "otp": otp,
                    "twofa": twofa,
                }
            },
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