import cv2
from PIL import Image
import binascii
import numpy as np
import codecs
import base64

## Take the image
cam = cv2.VideoCapture(0)
ret, frame = cam.read()

cv2.imwrite("transmission_image.png", frame)

cam.release()

## Simplify the image
image = Image.open('transmission_image.png').convert('LA')
image = image.resize((50, 50), Image.ANTIALIAS)
image.save('transmission_image.png', optimize = True, quality = 90)

## Convert to hexadecimal
data = open('transmission_image.png', 'rb').read()
data = binascii.hexlify(data)

## Convert to binary
scale = 16
num_of_bits = len(data)
data = bin(int(data, scale))[2:].zfill(num_of_bits)

## Convert to hexadecimal
data = str(hex(int(data, 2)))[2:-1]

## Convert to Base64
data = codecs.encode(codecs.decode(data, 'hex'), 'base64').decode()

## Convert to PNG
data = base64.b64decode(data)
with open('receive_image.png', 'wb') as f:
    f.write(data)


