import sys
import threading
import webview
from app import create_app

# Create Flask App
app = create_app()

def start_server():
    """Starts the Flask server in a separate thread."""
    # Use a specific port for the desktop app to avoid conflicts
    app.run(port=5001, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start Flask server in a thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # Create the native window
    # Validating port availability is good practice, but for simplicity:
    webview.create_window('Mikonku Hub', 'http://127.0.0.1:5001')
    
    # Start the GUI loop
    webview.start()
