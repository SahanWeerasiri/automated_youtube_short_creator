#!/bin/bash

# Destination folder in Pictures
DEST_DIR="$HOME/Pictures/Microsoft_Lockscreens"
mkdir -p "$DEST_DIR"

# Location of Microsoft lockscreen wallpapers
SRC_DIR="$HOME/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets"

# Find all files in source directory that are likely wallpapers (based on size)
find "$SRC_DIR" -type f | while read -r file; do
    # Get filename without path
    filename=$(basename "$file")
    
    # Generate destination filename with .jpg extension
    dest_file="$DEST_DIR/$filename.jpg"
    
    # Only copy if destination file doesn't exist
    if [[ ! -f "$dest_file" ]]; then
        cp "$file" "$dest_file"
        echo "Copied new wallpaper: $dest_file"
    fi
done

echo "Lockscreen wallpaper check complete."