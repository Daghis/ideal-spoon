from flask import Flask, render_template, request, session, redirect, url_for
import os

# Configuration for how many numbers appear in each level.
LEVEL_NUMBERS = {1: 9, 2: 16, 3: 25}

app = Flask(__name__)
app.secret_key = 'dev-secret-key'


def init_session():
    """Ensure tracking info exists in the session."""
    if 'completed' not in session:
        session['completed'] = []
        session.modified = True


def start_level(level: int):
    """Reset the current level state."""
    session['level'] = level
    total = LEVEL_NUMBERS.get(level, 9)
    session['numbers'] = list(range(1, total + 1))
    session['clicked'] = []
    session.modified = True


@app.route('/')
def root():
    init_session()
    return redirect(url_for('levels'))


@app.route('/levels')
def levels():
    init_session()
    max_level = max(LEVEL_NUMBERS)
    completed = set(session.get('completed', []))
    first_unsolved = None
    for lvl in range(1, max_level + 1):
        if lvl not in completed:
            first_unsolved = lvl
            break
    unlocked = completed.union({first_unsolved}) if first_unsolved else completed
    return render_template('levels.html', levels=range(1, max_level + 1), unlocked=unlocked)


@app.route('/level/<int:level>', methods=['GET', 'POST'])
def index(level):
    init_session()
    if level not in LEVEL_NUMBERS:
        return redirect(url_for('levels'))

    if session.get('level') != level or 'numbers' not in session:
        start_level(level)

    message = ''
    total = LEVEL_NUMBERS[level]

    if request.method == 'POST':
        num = int(request.form.get('num', 0))
        if num not in session['clicked']:
            session['clicked'].append(num)
            session.modified = True
        if len(session['clicked']) == total:
            message = 'Level complete!'
            if level not in session['completed']:
                session['completed'].append(level)
                session.modified = True

    next_level_enabled = len(session.get('clicked', [])) == total and level < max(LEVEL_NUMBERS)
    return render_template(
        'index.html',
        level=level,
        numbers=session['numbers'],
        clicked=session.get('clicked', []),
        message=message,
        next_level_enabled=next_level_enabled,
    )


@app.route('/restart')
def restart():
    level = session.get('level', 1)
    start_level(level)
    return redirect(url_for('index', level=level))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
