# Number Button Game

This is a simple web game where players press all numbered buttons. Early levels introduce ordering rules. It is implemented with Python using [Flask](https://flask.palletsprojects.com/).

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python app.py
   ```
3. Open your browser and go to `http://localhost:5000`.

## Files

- `app.py` – Flask application
- `templates/index.html` – HTML template
- `static/style.css` – basic styles
- `requirements.txt` – Python dependencies

## Testing

Run the unit tests with coverage enabled:

```bash
pytest --cov=. --cov-fail-under=70 -q
```

The repository includes a GitHub Actions workflow that installs dependencies and runs these tests with coverage reporting automatically on every push and pull request.

## Levels

The game starts at level 0 with a single button "1". Level 1 presents a 3×3 grid
and can be solved in any order. Level 2 uses the same grid but requires the
buttons be pressed in ascending order. Level 3 keeps the grid while the numbers
must be pressed in descending order. Later levels increase the total numbers and
the grid automatically grows to stay roughly square.
