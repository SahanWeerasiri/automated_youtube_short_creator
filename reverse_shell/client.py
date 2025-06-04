import cmd
import requests
import cv2
import numpy as np
import base64

API_URL = "http://192.168.1.2:5000/api/shell"
API_TOKEN = "your_secure_token_here"

class CameraViewer:
    def __init__(self):
        self.window_name = "Remote Camera Feed"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        self.run()
    
    def run(self):
        while True:
            try:
                response = requests.post(
                    API_URL,
                    headers={"Authorization": API_TOKEN, "Content-Type": "application/json"},
                    json={"command": "get camera frame"},
                    timeout=2
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "frame" in data:
                        frame_data = base64.b64decode(data["frame"].encode('utf-8'))
                        np_arr = np.frombuffer(frame_data, np.uint8)
                        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                        
                        if frame is not None:
                            cv2.imshow(self.window_name, frame)
                
                # Check for window close or ESC key
                key = cv2.waitKey(20)
                if (cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1) or (key == 27):
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Camera error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
        
        cv2.destroyAllWindows()

class RemoteShell(cmd.Cmd):
    prompt = "remote> "
    
    def __init__(self):
        super().__init__()
        self.headers = {
            "Authorization": API_TOKEN,
            "Content-Type": "application/json"
        }
        self.current_directory = "~"
    
    def update_prompt(self):
        self.prompt = f"remote:{self.current_directory}> "
    
    def default(self, line):
        if not line.strip():
            return
            
        try:                
            response = requests.post(
                API_URL,
                headers=self.headers,
                json={"command": line.strip()},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(data.get("output", ""))
                if "current_directory" in data:
                    self.current_directory = data["current_directory"]
                    self.update_prompt()
            else:
                print("Error:", response.json().get("error", "Unknown error"))
                
        except requests.exceptions.RequestException as e:
            print("Connection error:", e)
    
    def do_camera(self, arg):
        """Start camera viewer"""
        try:
            CameraViewer()
        except Exception as e:
            print(f"Failed to start camera: {e}")
    
    def do_exit(self, arg):
        """Exit the remote shell"""
        print("Goodbye!")
        return True
    
    def emptyline(self):
        pass

if __name__ == '__main__':
    shell = RemoteShell()
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")