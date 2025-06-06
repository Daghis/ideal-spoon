from flask import Flask, render_template, request, session, redirect, url_for
import os
import random

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

TOTAL_NUMBERS = 9


def start_game():
    session['numbers'] = random.sample(range(1, TOTAL_NUMBERS + 1), TOTAL_NUMBERS)
    session['index'] = 1
    session['clicked'] = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'numbers' not in session:
        start_game()

    message = ''

    if request.method == 'POST':
        num = int(request.form.get('num', 0))
        expected = session.get('index', 1)
        if num == expected:
            session['clicked'].append(num)
            session['index'] = expected + 1
            if expected == TOTAL_NUMBERS:
                message = 'Level complete!'
        else:
            message = 'Wrong button. Try again!'

    return render_template(
        'index.html',
        numbers=session['numbers'],
        clicked=session.get('clicked', []),
        message=message,
    )


@app.route('/restart')
def restart():
    start_game()
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
