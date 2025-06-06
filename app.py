from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

TOTAL_NUMBERS = 9


def start_game():
    """Initialize the game with numbers 1-9 in order."""
    session['numbers'] = list(range(1, TOTAL_NUMBERS + 1))
    session['clicked'] = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'numbers' not in session:
        start_game()

    message = ''

    if request.method == 'POST':
        num = int(request.form.get('num', 0))
        if num not in session['clicked']:
            session['clicked'].append(num)
        if len(session['clicked']) == TOTAL_NUMBERS:
            message = 'Level complete!'

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
