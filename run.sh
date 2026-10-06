
set -e

cd "$(dirname "$0")"

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Reusing existing virtual environment..."
fi

if [ -d "$VENV_DIR/bin" ]; then
    source "$VENV_DIR/bin/activate"
else
    source "$VENV_DIR/Scripts/activate"
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python -c "from app import create_app; create_app()"

echo "Starting API on http://127.0.0.1:5000"
python run.py