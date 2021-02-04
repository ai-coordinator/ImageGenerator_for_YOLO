#Python3で実行
import os,sys
import glob
from PIL import Image

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

try:
	sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
	pass
import cv2
abspath = os.path.dirname(os.path.abspath(__name__))

#リサイズしたい解像度を指定
width = 640
height = 640

#リサイズしたい画像をしたのディレクトリに格納
path = "./01_resize_before"
files = glob.glob(path + '/*.*')#画像の形式

print(files)
for i ,f in enumerate(files):
	print('{0}'.format(i,f))
	im = Image.open(str(f))
	# im_new = crop_max_square(im)
	im_new = crop_max_square(im).resize((width, height), Image.LANCZOS)
	im_new.save("./02_backgrounds" + '/ '+ '{0}'.format(i,f) + ".png", quality=95)
