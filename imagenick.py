#!/usr/bin/env python3.7
"""
This script reads a folder finding all images into it then
 generates for each image a new image with a name of its file without extension placed into bottom-right corner.
 Saves generated images into an output folder.
Usage: python imagenick.py -d images_dir -o output_dir
If -d is omitted the current path ($PWD) will be used.
If -o is omitted the ./output-images/ ($PWD/output-images/) will be used.
"""

__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-06-21'


import os
import argparse
import string
from PIL import Image, ImageDraw, ImageFont

# configuration
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
FONT_NAME = 'FreeSerif.ttf'
FONT_PATH = f"{SCRIPT_PATH}/{FONT_NAME}"
FONT_SIZE = 50  # font size in pixels
FONT_COLOR = (0, 255, 0)  # text color in RGB
PADDING_RIGHT = 15  # text block padding right in pixels
PADDING_BOTTOM = 15  # text block padding bottom in pixels


# FolderType for ArgumentParser
class FolderType(object):
    """Factory for creating folder object types

    Instances of FolderType are typically passed as type= arguments to the
    ArgumentParser add_argument() method.

    Keyword Arguments:
        - mode -- A string indicating the folder access mode: 'r' or 'w'.
    """

    def __init__(self, mode='r'):
        self._mode = mode

    def __call__(self, path):
        # all arguments are used as folder names
        if not os.path.isdir(path):
            message = "'%s' in not a directory"
            raise argparse.ArgumentTypeError(message % path)
        if not os.access(path, os.X_OK):
            message = "directory access error '%s' is not executable"
            raise argparse.ArgumentTypeError(message % path)
        if self._mode == 'r':
            if not os.access(path, os.R_OK):
                message = "directory access error '%s' is not readable"
                raise argparse.ArgumentTypeError(message % path)
        elif self._mode == 'w':
            if not os.access(path, os.R_OK):
                message = "directory access error '%s' is not writable"
                raise argparse.ArgumentTypeError(message % path)
        return path

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._mode)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""This script reads a folder finding all images into it then
 generates for each image a new image with a name of its file without extension placed into bottom-right corner.
 Saves generated images into an output folder.""")
    parser.add_argument('-d', nargs=1, type=FolderType('r'), metavar='IMAGES PATH',
                        help='path to images folder, using current path if omitted')
    parser.add_argument('-o', nargs=1, type=FolderType('w'), metavar='OUTPUT PATH',
                        help='path to output folder, using ./output-images/ if omitted')
    args = parser.parse_args()
    images_dir = args.d[0] if args.d else os.getcwd()
    output_dir = args.o[0] if args.o else f"{os.getcwd()}/output-images"
    print(args)
    if not os.path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except Exception as e:
            message = _("Error: '%s' could not be created")
            print(message % output_dir)
            exit(1)
    for r, d, f in os.walk(images_dir):
        for file in f:
            if os.access(f"{r}/{file}", os.R_OK):
                if file.lower().endswith('.png'):
                    extension = 'png'
                elif file.lower().endswith('.jpg'):
                    extension = 'jpg'
                elif file.lower().endswith('.jpeg'):
                    extension = 'jpeg'
                else:
                    # skip file
                    print(f"skip file '{r}/{file}' unsupported extension")
                    continue
                # getting the text to placing into the image
                image_text = "\xa9 "+string.capwords(file.replace('-', ' ').replace(f".{extension}", ''))
                # getting image width and height in pixels
                with Image.open(f"{r}/{file}") as img:
                    image_width, image_height = img.size  # getting image size
                    print(f"file '{r}/{file}' width={image_width}, height={image_height}")
                    drawer = ImageDraw.Draw(img)  # init Drawer
                    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)  # creating font
                    text_width, text_height = drawer.textsize(image_text, font=font)
                    print(f"text '{image_text}' size: width={text_width}, height={text_height}")
                    # checking sizes
                    if image_width < (text_width+PADDING_RIGHT) or image_height < (text_height+PADDING_BOTTOM):
                        print(f"Error: the image '{r}/{file}' is too small.")
                        continue
                    # calc the text coordinates
                    text_x = image_width - text_width - PADDING_RIGHT
                    text_y = image_height - text_height - PADDING_BOTTOM
                    # draw the text
                    drawer.text((text_x, text_y), image_text, font=font, fill=FONT_COLOR)
                    # save the image
                    img.save(f"{output_dir}/{file}")
            else:
                print(f"skip file '{r}/{file}' access denied")
