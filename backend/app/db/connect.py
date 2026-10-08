import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="welcome@123",
    database="llm"
)

print("Connected")

cursor = conn.cursor(dictionary= True)