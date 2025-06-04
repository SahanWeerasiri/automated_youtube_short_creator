# README

## Project Overview

`save_lockscreens.sh`: This file likely contains a script, potentially for saving or managing lock screen images.


## Project Structure

The project structure is as follows:

```
- save_lockscreens.sh
```

## Project Details

This project contains the following files:

- save_lockscreens.sh
### save_lockscreens.sh
This bash script automates the process of copying Microsoft Windows lockscreen wallpapers to a designated folder within your Pictures directory.

Here's a breakdown:

1. **Sets up the destination directory:** It creates the directory `$HOME/Pictures/Microsoft_Lockscreens` if it doesn't already exist. This is where the wallpapers will be copied.

2. **Defines the source directory:**  It points to the location where Windows stores the lockscreen wallpapers: `$HOME/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets`.

3. **Finds potential wallpaper files:** It uses `find` to locate all files within the source directory.

4. **Loops through each potential wallpaper file:**  The `while` loop iterates through each file found.

5. **Constructs the destination filename:**  For each file, it gets the filename and adds the `.jpg` extension, creating the full path for the copied file in the destination directory.

6. **Checks for existing files:** It checks if a file with the same name (including the `.jpg` extension) already exists in the destination directory.

7. **Copies if necessary:** If the destination file doesn't exist, it copies the file from the source to the destination, effectively renaming it to include the `.jpg` extension. It then prints a message indicating that a new wallpaper was copied.

8. **Completion message:** Finally, it prints a message indicating the script has finished running.

In essence, the script finds and copies new lockscreen wallpapers from the Windows system directory to a user-friendly location in the Pictures folder, adding a `.jpg` extension, and avoiding duplicates.


