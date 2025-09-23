from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Development mode
    port = int(os.environ.get('PORT', 8080))
    app.run(host="127.0.0.1", port=port, debug=False)