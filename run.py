import os
import sys

# Ensure the project root (this directory) is on the Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app import create_app

app = create_app()

if __name__ == '__main__':
    import os
    try:
        port = int(os.environ.get('PORT', '5000'))
    except Exception:
        port = 5000
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)
