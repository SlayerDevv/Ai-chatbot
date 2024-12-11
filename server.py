from flask import Flask, request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import json

app = Flask(__name__)


template = """
You are an expert AI assistant with advanced programming skills, capable of helping with complex code generation, debugging, and explaining technical concepts. You can assist with tasks such as explaining algorithms, solving code issues, generating snippets, and providing advice on best practices. Additionally, you are also a helpful chatbot that can converse on any topic, offer advice, and engage with users in a friendly and informative manner.

Context: {context}
Input: {user_input}
"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.2:latest")
chain = prompt | model


@app.route("/chat", methods=["POST"])
def chat():
    if request.is_json:
        req = request.get_json()
        payload = req.get("payload")
        if not payload:
            return jsonify({"error": "Invalid payload"}), 400
    else:
        message = request.form.to_dict()
        if not message or not message.get("payload"):
            return jsonify({"error": "Invalid input"}), 400
        payload = message.get("payload")
    try:
        response = chain.invoke({"user_input": payload, "context": ""})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    result = jsonify({"response": response})
    return result


if __name__ == "__main__":
    app.run(debug=True)
