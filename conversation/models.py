from flask import jsonify
import uuid
from app import db
import datetime


conversations_collection = db["conversations"]


class Conversation:
    def Create(self, ownerId):
        conversation = {
            "_id": uuid.uuid4().hex,
            "systemMessages": [],
            "userMessages": [],
            "ownerId": ownerId,
            "metadata": {
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now(),
            },
        }
        conversations_collection.insert_one(conversation)
        return jsonify({"error": "", "success": "true", "data": conversation}), 200

    def Update(self, conversation_id, conversation_owner, type, data):

        conversation = conversations_collection.find_one(
            {"_id": conversation_id, "ownerId": conversation_owner}
        )

        if not conversation:
            return (
                jsonify(
                    {
                        "error": "Conversation not found",
                        "success": "false",
                        "data": None,
                    }
                ),
                200,
            )

        if type == "user":
            conversation["userMessages"].append(data)
        elif type == "system":
            conversation["systemMessages"].append(data)

        conversation["metadata"]["updated_at"] = datetime.datetime.now()

        conversations_collection.update_one(
            {"_id": conversation_id}, {"$set": conversation}
        )

        return jsonify({"error": "", "success": "true", "data": conversation}), 200

    def Delete(self, conversation_id):
        conversation_owner = conversations_collection.find_one(
            {"_id": conversation_id}
        )["ownerId"]
        conversations_collection.delete_one({"_id": conversation_id})
        db.users.update_one(
            {"_id": conversation_owner},
            {"$pull": {"conversations_ids": conversation_id}},
        )
        return (
            jsonify(
                {
                    "error": "",
                    "success": "true",
                    "message": f"Convesation with Id {conversation_id} has been deleted",
                    "data": None,
                }
            ),
            200,
        )
