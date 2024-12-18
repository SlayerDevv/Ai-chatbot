from flask import Flask, request, jsonify
from app import app
from conversation.models import Conversation


@app.route("/conversation/create", methods=["POST"])
def create_conversation():
    if request.is_json:
        data = request.get_json()
        ownerId = data.get("ownerId")
        Conversation().Create(ownerId)
        return jsonify({"error": "", "message": "Conversation created successfuly"})


@app.route("/conversation/delete", methods=["DELETE"])
def delete_conversation():
    if request.is_json:
        data = request.get_json()
        conversationId = data.get("conversationId")
        Conversation().Delete(conversationId)
        return jsonify({"error": "", "message": "Conversation deleted successfuly"})
