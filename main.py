from flask import Flask, render_template, request, redirect
import socket
import json
from datetime import datetime

app = Flask(__name__)

# Определение пути для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Определение пути для страницы сообщений
@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        save_message(username, message)
        return redirect('/message')
    else:
        return render_template('message.html')

# Сохранение сообщения в файл data.json
def save_message(username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data = {
        timestamp: {
            'username': username,
            'message': message
        }
    }
    with open('storage/data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

# Определение пути для страницы ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Запуск Flask сервера
def run_flask_server():
    app.run(port=3000)

# Запуск Socket сервера
def run_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))

    while True:
        message, _ = server_socket.recvfrom(1024)
        save_socket_message(message.decode())

# Сохранение сообщения от Socket сервера
def save_socket_message(message):
    try:
        data = json.loads(message)
        save_message(data['username'], data['message'])
    except (json.JSONDecodeError, KeyError):
        pass

if __name__ == '__main__':
    import threading

    # Запуск HTTP сервера в отдельном потоке
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.start()

    # Запуск Socket сервера в отдельном потоке
    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()
