"""from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
"""

from app import create_app
import os

env = os.environ.get("FLASK_ENV", "development")

app = create_app()  # <-- sin argumentos

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=(env == "development")
    )
