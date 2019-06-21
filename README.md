# imagenick

This script reads a folder finding all images into it then
 generates for each image a new image with a name of its file without extension placed into bottom-right corner.
 Saves generated images into an output folder.
Usage: python imagenick.py -d images_dir -o output_dir
If -d is omitted the current path ($PWD) will be used.
If -o is omitted the ./output-images/ ($PWD/output-images/) will be used.

REQUIREMENTS:
    python 3.7
    pillow

