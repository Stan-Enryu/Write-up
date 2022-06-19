#!/usr/bin/env python3

import pytesseract
from PIL import Image
import PIL.ImageOps
import requests

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
URL = 'http://challenge.ctf.games:32125'

for i in range(46):
    image_request = requests.get(f'{URL}/static/otp.png', stream = True)
    with open('otp.png', 'wb') as fd:
        for chunk in image_request.iter_content(chunk_size=128):
            fd.write(chunk)
    image = Image.open('otp.png')
    # Preprocess the image by converting it from white text on black, to black text on white. 
    # (Provides more accurate recognition.)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save('otp-inverted.png')

    # Perform optical character recognition
    # Configuration:
    # -psm 6 : Set analysis mode to assume a single uniform block of text
    # -oem 3 : Use default OCR Engine mode
    # -l eng : Recognize English character set
    # -c tessedit_char_whitelist=0123456789 : Only recognize digits
    code = pytesseract.image_to_string(
             Image.open('otp-inverted.png'), 
             config='--psm 6 --oem 3 -l eng -c tessedit_char_whitelist=0123456789'
           ).strip()
    print(code)

    post = requests.post(URL, data={'otp_entry': code})
    print(post.text)