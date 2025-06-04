from flask import Flask, jsonify, request
import subprocess
import os
import logging
from threading import Lock

app = Flask(__name__)
API_TOKEN = "your_secure_token_here"
current_directory = os.path.expanduser("~")  # Start in user's home directory
dir_lock = Lock()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)