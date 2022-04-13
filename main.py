from flask import Flask, render_template, request
import datetime
import json

app = Flask(__name__)

DB_FILE = "./data/db.json"
db = open(DB_FILE, "rb")
data = json.load(db)
messages = data["messages"]



def save_to_file():
    db = open(DB_FILE, "w")
    data = {
        "messages": messages
    }
    json.dump(data, db)


def add_message(text, sender): # Объявим функцию добавления сообщения
    now = datetime.datetime.now()
    new_message = {
        "text": text,
        "sender": sender,
        "time": now.strftime("%H:%M %d-%m-%Y")
    }
    messages.append(new_message)
    save_to_file()

def print_message(message):  # Объявляем функцию которая будет печатать 1 сообщение
    print(f" [{message['sender']}]: {message['text']} / {message['time']}")

# Главная страница
@app.route("/")
def index_page():
    return "Здравствуйте, Вас приветствует Поняшка ^_^"

# Показать сообщения чата в формате JSON
@app.route("/get_messages")
def get_messages():
    return { "messages": messages}

# Показать форму чата
@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/send_message")
def send_message():
    # Получить имя и сообщение пользователя
    name = request.args["name"]
    text = request.args["text"]
    if len(name) < 3 or len(name) > 100:
        print("Недопустимая длина имени")
    elif len(text) < 1 or len(text) > 1000:
        print("Недопустимая длина сообщения")
    else:
         # Вызвать функцию add_message
        add_message(text, name)
    return "OK"

app.run() # Запуск веб-приложения

