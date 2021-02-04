""""backgroundに背景画像，itemsに物体画像を入れてPython3で実行"""
from time import sleep
import sys
import shutil
#ROSのCV2とpython3のCV2がコンフリクトする人向け
try:
	sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
	pass
import cv2
import numpy as np
import glob
from lib.image_generator import *
from lib.yolabelgenerator import *

trainfolder = "train/"
validfolder = "valid/"
num = 100
trainnum = num * 9
validnum = num

item_path = "./items/"#合成したい物体のパス
background_path = "./02_backgrounds/"#合成先の背景のパス
Generate_folder = "./03_output/"#合成後のデータセットを格納するディレクトリ
seriesname = "sample_"
#合成後のデータセットの頭に付くファイル名
#ラベルをファイルの頭に付けて分離したほうがやりやすい(0クラスなら:0data_)

size = 416

def restrict_value_in_image(anno, width, height):
	xmin = max(anno[0], 0)
	xmax = min(anno[1], width)
	ymin = max(anno[2], 0)
	ymax = min(anno[3], height)
	return [xmin, xmax, ymin, ymax]

def get_annotation_value(box):
	#box_x,box_y,box_w,box_hs
	x = box[1]
	y = box[2]
	w = box[3]
	h = box[4]
	xmin = int(x - w / 2)
	xmax = int((x + w / 2))
	ymin = int(y - h / 2)
	ymax = int((y + h / 2))
	return [xmin, xmax, ymin, ymax]

def get_classname(filename):
	classname = filename.split("-")[0]
	return classname

def generator_set(number, size):
	n_samples = number #1セットに作成する画像枚数
	n_items = 1 # 1画像中に合成する物体の数
	#合成後のデータセットの解像度,実際の環境に合わせる(Kinect-h:480w:640)
	input_width = size
	input_height = size
	#それぞれ0でそのまま
	min_item_scale = 0.2  # 物体の縮小率
	max_item_scale = 1.3 # 物体の拡大率
	rand_angle = 90  # 物体の回転角度
	minimum_crop = 0.85
	delta_hue = 0.0  #HSV空間における色相の変化量
	delta_sat_scale = 0.3  #HSV空間における彩度の変化量
	delta_val_scale = 0.3  #HSV空間における明度の変化量
	range_of_overlay = [[0, 480], [80, 415]]  #物体生成の範囲制限[[xmin,xmax],[ymin,ymax]]
	generate_once = True

	# "label-"でラベルを分離する．(0-file.pngのような形式)
	generator = ImageGenerator(item_path, background_path, split_class="-")

	x, t = generator.generate_samples(
		n_samples=n_samples,
		n_items=n_items,
		crop_width=input_width,
		crop_height=input_height,
		min_item_scale=min_item_scale,
		max_item_scale=max_item_scale,
		rand_angle=rand_angle,
		minimum_crop=minimum_crop,
		delta_hue=delta_hue,
		delta_sat_scale=delta_sat_scale,
		delta_val_scale=delta_val_scale,
		range_of_overlay=range_of_overlay,
		generate_once=generate_once
	)
	return x, t


def annotation(x, t, input_width, input_height, folder):
	number = 1
	yamllist = []
	for i, image in enumerate(x):
		image = np.transpose(image, (1, 2, 0)).copy()
		dataname = seriesname + "{}".format(number)
		# imagename = dataname + ".png"
		trainfolder = folder
		anofolder = Generate_folder + trainfolder + "images/"
		labelsfolder = Generate_folder + trainfolder + "labels/"

		Imagepath = anofolder + dataname + ".png"
		TXTpath = labelsfolder + dataname + ".txt"  # YOLO用のラベルパスの定義

		if not os.path.isdir(anofolder):
			os.makedirs(anofolder)
		if not os.path.isdir(labelsfolder):
			os.makedirs(labelsfolder)

			text_file = open(labelsfolder + "/classes.txt", "w")
			files = os.listdir(item_path)
			files = sorted(files)
			for f in files:
				basename_without_ext,ext = os.path.splitext(os.path.basename(f)) # 拡張子抜きのファイル名を取得
				objectname = basename_without_ext.split("-")
				print('通過',objectname[-1])
				text_file.write(objectname[-1] + "\n") # テキストファイルに書き込む
				yamllist.append(objectname[-1])
			text_file.close()

		width, height, _ = image.shape

		image = (image * 255).astype('uint8')
		cv2.imwrite(Imagepath, image * 255)

		for truth_box in t[i]:
			box_x, box_y, box_w, box_h = truth_box['x'], truth_box['y'], truth_box['w'], truth_box['h']
			classname = truth_box['classname']
			box = [classname, box_x, box_y, box_w, box_h]
			#print(box)
			anno = get_annotation_value(box)
			anno = restrict_value_in_image(anno, input_width, input_height)
			# YOLO用のラベル形式を作成
			writeyolabel(TXTpath, dataname, box)
		# image = (image * 255).astype('uint8')
		# Imagefolder = Generate_folder + "images/"

		# if not os.path.isdir(Imagefolder):
		# 	os.makedirs(Imagefolder)
		# cv2.imwrite(Imagepath, image * 255)
		number = number + 1
	# print("Set " + str(set + 1) + " Done.")
	# sleep(5)#落ちるので止める
	yaml_file = open(Generate_folder + "/data.yaml", "w")
	yaml_file.write('train: train/images' + "\n")
	yaml_file.write('val: valid/images' + "\n")
	yaml_file.write('' + "\n")
	yaml_file.write('nc: ' + str(len(files)) + "\n")
	yaml_file.write('names: ' + str(yamllist) + "\n")
	yaml_file.close()

if __name__ == '__main__':

	if os.path.isdir(Generate_folder + trainfolder):
		shutil.rmtree(Generate_folder + trainfolder)
	if os.path.isdir(Generate_folder + validfolder):
		shutil.rmtree(Generate_folder + validfolder)

	#tarinデータ作成
	x, t = generator_set(trainnum, size)
	annotation(x, t, size, size, trainfolder)

	#validデータ作成
	x, t = generator_set(validnum, size)
	annotation(x, t, size, size, validfolder)

	print("Generate Finished.")
