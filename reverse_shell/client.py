import cmd
import requests
import json

API_URL = "http://192.168.52.215:5000/api/shell"
API_TOKEN = "your_secure_token_here"

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
                json={"command": line.strip()}
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
    
    def do_exit(self, arg):
        """Exit the remote shell"""
        print("Goodbye!")
        return True
    
    def emptyline(self):
        pass

if __name__ == '__main__':
    RemoteShell().cmdloop()