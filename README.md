# 💸 FinPal – Financial Literacy for Kids with Real Bank Data + AI

**FinPal** is a web app designed to help kids and young teens understand money by linking their real bank accounts (with parental permission) and interacting with a friendly AI chatbot that explains financial concepts in an engaging way.

Built with Plaid and ChatGPT, the platform allows users to view their spending, savings, and banking activity while receiving age-appropriate explanations and guidance — all within a secure, kid-friendly interface.

---

## 🚀 Tech Stack

- **Backend**: Django
- **Frontend**: JavaScript, HTML, CSS
- **Database**: AWS DynamoDB

---

## 🛠️ Installation Instructions

> ⚠️ Note: This project does **not use a virtual environment** for simplicity.

1. **Clone the repository**  
```bash
git clone https://github.com/JackXuCatch22/Ramblin-Hacks2025.git
cd Ramblin-Hacks2025/frontend
```

2. **Install required packages**
```bash
pip install boto3
pip install bcrypt
pip install dotenv
pip install djangorestframework
pip install openai
```

3. **Create a .env file in the root directory with the following variables:**
```bash
AWS_ACCESS_KEY_ID_dynamo=your_aws_access_key
AWS_SECRET_ACCESS_KEY_dynamo=your_aws_secret_key
```

4. **Run the Django server**
```bash
python manage.py runserver
```

5. **Open your browser and visit http://127.0.0.1:8000/**


🔐 Security & Data Privacy

    All financial data is securely accessed through Plaid and never stored directly.

    User authentication is handled with bcrypt hashing.

    Environment secrets are stored in .env and should never be committed to version control.

🤖 Features

    🔗 Link real bank accounts using Plaid (with parental consent)

    💬 Ask questions to a ChatGPT-powered chatbot trained to explain financial terms simply

    📊 View real-time balances, categorized transactions, and spending summaries

    🎯 Designed specifically for younger audiences learning about money
