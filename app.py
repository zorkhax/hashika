#!/usr/bin/env python
from app import app


if __name__ == "__main__":
    app.run(port=5432, debug=True, host='0.0.0.0')
