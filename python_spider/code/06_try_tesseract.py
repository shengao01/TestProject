# coding=utf-8
import pytesseract
from PIL import Image

file_path = "/Users/zdw/Documents/工作/备课/爬虫/图片/tesseracttest1.jpg"
file_path = "/Users/zdw/Documents/工作/备课/爬虫/图片/tess2.jpg"
img = Image.open(file_path)
t1 = pytesseract.image_to_string(img)
print(t1)