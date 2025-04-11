from flask import Flask, request, jsonify, render_template_string
import requests
from markdown2 import markdown  # لتحويل النصوص إلى HTML يدعم Markdown
import mysql.connector  # للاتصال بقاعدة البيانات MySQL

app = Flask(__name__)

# رابط Rasa
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

# إعدادات قاعدة البيانات
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # استبدل باسم المستخدم الخاص بك
    "password": "123",  # استبدل بكلمة المرور الخاصة بك
    "database": "admission_db"
}

# دالة للاتصال بقاعدة البيانات
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

HTML_TEMPLATE =""""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Admission Enquiry Assistant</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background-color: #f5f5f5;
    }

    .chat-widget-button {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background-color: #004080; /* أزرق */
      border: none;
      border-radius: 50%;
      width: 60px;
      height: 60px;
      padding: 8px;
      cursor: pointer;
      z-index: 1000;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .chat-widget-button img {
      width: 35px;
      height: 35px;
      object-fit: contain;
    }

    .chat-container {
      position: fixed;
      bottom: 95px;
      right: 20px;
      width: 340px;
      height: 500px;
      background-color: #ffffff;
      border-radius: 16px;
      box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.2);
      display: none;
      flex-direction: column;
      overflow: hidden;
      z-index: 999;
    }

    .chat-header {
      background-color: #004080;
      color: #ffffff;
      padding: 15px;
      font-size: 18px;
      text-align: center;
    }

    .chat-box {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      background-color: #e6f0ff;
    }

    .chat-message {
      margin: 8px 0;
      display: flex;
      align-items: flex-start;
    }

    .chat-message.user {
      justify-content: flex-start;
    }

    .chat-message.user .message {
      background-color: #d1f8d1;
      color: #000;
      border-radius: 15px 15px 0 15px;
      padding: 10px;
      max-width: 75%;
      font-size: 14px;
      word-wrap: break-word;
    }

    .chat-message.bot {
      justify-content: flex-end;
    }

    .chat-message.bot .message {
      background-color: #ffffff;
      color: #2c3e50;
      border-radius: 15px 15px 15px 0;
      padding: 10px;
      max-width: 75%;
      font-size: 14px;
      word-wrap: break-word;
      box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }

    .input-container {
      display: flex;
      align-items: center;
      padding: 10px;
      background-color: #fff;
      border-top: 1px solid #ccc;
    }

    .input-container input {
      flex: 1;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 20px;
      font-size: 14px;
      background-color: #f9f9f9;
      outline: none;
      margin-left: 10px;
    }

    .input-container button {
      background-color: #004080;
      color: #ffffff;
      border: none;
      border-radius: 50%;
      width: 36px;
      height: 36px;
      font-size: 18px;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <!-- زر فتح الشات بشكل دائري باللون الأزرق -->
  <button class="chat-widget-button" onclick="toggleChat()">
    <img src="https://downloads.intercomcdn.com/i/o/378475/452a29d68866e874f9ddccf0/9e0f012f15b6fc981dde2f1f5198d728.png" alt="Chat Icon">
  </button>

  <!-- نافذة الشات -->
  <div class="chat-container" id="chat-container">
    <div class="chat-header">مساعد القبول والتسجيل</div>
    <div class="chat-box" id="chat-box"></div>
    <div class="input-container">
      <input type="text" id="user-message" placeholder="اكتب رسالتك هنا...">
      <button onclick="sendMessage()">&#10148;</button>
    </div>
  </div>

  <script>
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-message");
    const chatContainer = document.getElementById("chat-container");
    let typingIndicator;

    function toggleChat() {
      const isVisible = chatContainer.style.display === "flex";
      chatContainer.style.display = isVisible ? "none" : "flex";

      if (!isVisible && chatBox.childElementCount === 0) {
        addMessage("مرحباً بك 👋! أنا مساعد القبول والتسجيل. كيف يمكنني مساعدتك؟", "bot");
      }
    }

    function addMessage(content, sender = "bot") {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("chat-message", sender);

      const messageContent = document.createElement("div");
      messageContent.classList.add("message");

      messageContent.innerHTML = content;
      messageDiv.appendChild(messageContent);
      chatBox.appendChild(messageDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTyping() {
      if (!typingIndicator) {
        typingIndicator = document.createElement("div");
        typingIndicator.classList.add("chat-message", "bot");
        typingIndicator.innerHTML = '<div class="message">جاري الكتابة...</div>';
        chatBox.appendChild(typingIndicator);
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }

    function hideTyping() {
      if (typingIndicator) {
        chatBox.removeChild(typingIndicator);
        typingIndicator = null;
      }
    }

    async function sendMessage() {
      const message = userInput.value.trim();
      if (!message) return;

      addMessage(message, "user");
      userInput.value = "";

      showTyping();

      try {
        const response = await fetch("/webhook", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: message }),
        });

        const data = await response.json();
        hideTyping();

        const botMessage = data.response || "عذرًا، لم أفهم رسالتك.";
        addMessage(botMessage, "bot");
      } catch (error) {
        hideTyping();
        addMessage("حدث خطأ أثناء الاتصال بـ Rasa.", "bot");
      }
    }

    userInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        sendMessage();
      }
    });
  </script>
</body>
</html>

"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/webhook", methods=["POST"])
def webhook():
    user_message = request.json.get("message", "").strip()

    try:
        response = requests.post(RASA_SERVER_URL, json={"sender": "user", "message": user_message})
        response.raise_for_status()
        bot_responses = response.json()

        response_text = bot_responses[0].get("text", "عذرًا، لم أفهم رسالتك.") if bot_responses else "عذرًا، لم أفهم رسالتك."
        response_html = markdown(response_text)

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Rasa: {e}")
        response_html = "حدث خطأ أثناء الاتصال بـ Rasa."

    return jsonify({"response": response_html})

@app.route('/fees', methods=['GET'])
def get_fees():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # جلب البيانات من جدول admission_fees
        cursor.execute("SELECT admission_type, fees_amount FROM admission_fees")
        fees_data = cursor.fetchall()

        cursor.close()
        connection.close()

        # إرجاع البيانات كـ JSON
        return jsonify(fees_data)

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return jsonify({"message": "حدث خطأ أثناء الاتصال بقاعدة البيانات"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)