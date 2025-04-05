def generate_chatgpt_data(question):

    print("🌍 question received:", question)

    if not country:
        return jsonify({"error": "No country provided"}), 400

    prompt = f"""Using your training data, give good financial advice and answer the user's question: {question}"""


    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content
    print("🧠 GPT-4 responded with:\n", content)

    return content
