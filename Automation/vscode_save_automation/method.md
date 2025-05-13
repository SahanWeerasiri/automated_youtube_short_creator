### **Method 1: Using VSCode Tasks + Keyboard Shortcut**
1. **Create a Task in VSCode**:
   - Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
   - Type `Tasks: Configure Task` and select it.
   - Choose `Create tasks.json file from template` → `Others`.
   - Replace the content with:
     ```json
     {
       "version": "2.0.0",
       "tasks": [
         {
           "label": "Run Batch File",
           "type": "shell",
           "command": "${workspaceFolder}/yourfile.bat", // Update path to your .bat file
           "problemMatcher": []
         }
       ]
     }
     ```
   - Save the file (`tasks.json`).

2. **Assign a Keyboard Shortcut**:
   - Open the Command Palette again (`Ctrl+Shift+P`).
   - Type `Preferences: Open Keyboard Shortcuts (JSON)`.
   - Add this entry:
     ```json
     {
       "key": "ctrl+alt+b", // Choose your preferred hotkey
       "command": "workbench.action.tasks.runTask",
       "args": "Run Batch File"
     }
     ```
   - Save the file.

Now, pressing `Ctrl+Alt+B` (or your chosen hotkey) will execute the `.bat` file.

---

### **Method 2: Using a VSCode Extension (Advanced)**
If you need more control (like running in a terminal), you can use the **Terminal Commands** extension:
1. Install the [Terminal Commands](https://marketplace.visualstudio.com/items?itemName=usernamehw.terminal-commands) extension.
2. Configure a command in `settings.json`:
   ```json
   "terminalCommands.commands": {
     "Run Batch File": "yourfile.bat"
   }
   ```
3. Assign a hotkey in `keybindings.json`:
   ```json
   {
     "key": "ctrl+alt+b",
     "command": "terminalCommands.runCommand",
     "args": "Run Batch File"
   }
   ```

---

### **Notes**
- Ensure the `.bat` file is in your workspace or provide the full path (`C:/path/to/yourfile.bat`).
- If the script requires admin rights, you may need additional setup (like running VSCode as admin).
