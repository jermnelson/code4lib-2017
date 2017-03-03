import hashlib
import os
from __init__ import app

if not "SECRET_KEY" in app.config or app.config.get("SECRET_KEY") is None:
    app.config["SECRET_KEY"] = hashlib.sha256(os.urandom(45)).hexdigest()

if __name__ == "__main__":
    # Initialized content
    app.run(debug=True, host="0.0.0.0", port=5005)
