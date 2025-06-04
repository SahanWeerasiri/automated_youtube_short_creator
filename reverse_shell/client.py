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
        self.running = True
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        # Start camera on server
        try:
            response = requests.post(
                API_URL,
                headers={"Authorization": API_TOKEN, "Content-Type": "application/json"},
                json={"command": "start camera"},
                timeout=2
            )
            if response.status_code != 200:
                raise Exception("Failed to start camera on server")
        except Exception as e:
            print(f"Error starting camera: {e}")
            self.running = False
            return

        self.run()

    def run(self):
        while self.running:
            try:
                # Get frame from server
                response = requests.post(
                    API_URL,
                    headers={"Authorization": API_TOKEN, "Content-Type": "application/json"},
                    json={"command": "get camera frame"},
                    timeout=1
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "frame" in data:
                        frame_data = base64.b64decode(data["frame"].encode('utf-8'))
                        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                        if frame is not None:
                            cv2.imshow(self.window_name, frame)
                
                # Check for exit conditions
                if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                    self.stop()
                    break
                    
                if cv2.waitKey(1) == 27:  # ESC key
                    self.stop()
                    break
                    
            except requests.exceptions.RequestException as e:
                if not self.running:  # If we're stopping, ignore errors
                    break
                print(f"Camera error: {e}")
                self.stop()
                break

    def stop(self):
        if self.running:
            self.running = False
            try:
                # Stop camera on server
                requests.post(
                    API_URL,
                    headers={"Authorization": API_TOKEN, "Content-Type": "application/json"},
                    json={"command": "stop camera"},
                    timeout=1
                )
            except:
                pass  # Ensure we always close the window even if stop fails
            
            try:
                cv2.destroyWindow(self.window_name)
            except:
                pass

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
        """Start camera viewer (press ESC or close window to stop)"""
        try:
            viewer = CameraViewer()
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