import mysql.connector

def get_admission_fees(admission_type):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="admission_db"
    )
    cursor = connection.cursor()
    query = "SELECT fees_amount FROM admission_fees WHERE admission_type = %s"
    cursor.execute(query, (admission_type,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None

def save_conversation(user_message, bot_response):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="admission_db"
    )
    cursor = connection.cursor()
    query = "INSERT INTO conversations (user_message, bot_response) VALUES (%s, %s)"
    cursor.execute(query, (user_message, bot_response))
    connection.commit()
    cursor.close()
    connection.close()