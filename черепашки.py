# web_app.py
from flask import Flask, render_template, jsonify
import random
import threading

app = Flask(__name__)

# Состояние черепашек (будет обновляться)
turtles_state = []
colors = ['red', 'yellow', 'blue', 'green', 'purple', 'orange', 'pink']


def generate_turtles():
    global turtles_state
    # Создаем позиции как в вашем коде
    positions = [
        (0, 113), (10, 85), (-10, 85), (30, 60), (10, 60), (-10, 60), (-30, 60),
        (-50, 35), (-30, 35), (-10, 35), (10, 35), (30, 35), (50, 35),
        (-70, 10), (-50, 10), (-30, 10), (-10, 10), (10, 10), (30, 10), (50, 10), (70, 10),
        (-90, -15), (-70, -15), (-50, -15), (-30, -15), (-10, -15), (10, -15),
        (30, -15), (50, -15), (70, -15), (90, -15), (3, -40), (3, -65)
    ]

    turtles_state = []
    for i, (x, y) in enumerate(positions[:31]):  # Первые 31 - зеленые
        turtles_state.append({
            'id': i + 1,
            'x': x,
            'y': y,
            'color': 'green',
            'is_green': True
        })

    # Добавляем коричневые
    for i, (x, y) in enumerate(positions[31:]):
        turtles_state.append({
            'id': i + 32,
            'x': x,
            'y': y,
            'color': 'brown',
            'is_green': False
        })

    # Добавляем желтую (звезду)
    turtles_state.append({
        'id': 34,
        'x': 0,
        'y': 140,
        'color': 'yellow',
        'is_green': False,
        'is_star': True
    })


# Функция для анимации мигания
def animate_turtles():
    while True:
        time.sleep(0.5)
        for i, turtle in enumerate(turtles_state):
            if turtle.get('is_green', False):
                # Меняем цвет случайным образом
                if random.random() > 0.7:
                    turtle['color'] = random.choice(colors)
                    turtle['animating'] = True
                    turtle['animation_step'] = 0
                else:
                    turtle['color'] = 'green'
                    turtle['animating'] = False


# Запускаем в отдельном потоке
import time

generate_turtles()
threading.Thread(target=animate_turtles, daemon=True).start()


@app.route('/')
def index():
    return render_template('turtle_tree.html')


@app.route('/api/turtles')
def get_turtles():
    return jsonify(turtles_state)


@app.route('/api/animate/<int:turtle_id>')
def animate_turtle(turtle_id):
    for turtle in turtles_state:
        if turtle['id'] == turtle_id and turtle.get('is_green', False):
            turtle['color'] = random.choice(colors)
            turtle['animating'] = True
            turtle['animation_step'] = 0
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
