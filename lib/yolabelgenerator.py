def prepareXML(xml_path, filename, width, height, depth=3):
	with open(xml_path, 'w') as voc:
		line = '<annotation>\n'
		voc.write(line)
		# line = '\t<folder>' + noised_dataraw + '</folder>\n'
		# print head
		# voc.write(line)
		line = '\t<filename>' + filename + '</filename>\n'
		voc.write(line)
		# keyboard()
		# line = '\t<path>' + os.path.abspath(os.path.join(root,imgfile)) + '</path>\n'
		# voc.write(line)
		line = '\t<source>\n'
		voc.write(line)
		line = '\t\t<database>Unknown</database>\n'
		voc.write(line)
		line = '\t</source>\n'
		voc.write(line)
		line = '\t<size>\n'
		voc.write(line)
		line = '\t\t<width>' + str(width) + '</width>\n'
		voc.write(line)
		line = '\t\t<height>' + str(height) + '</height>\n'
		voc.write(line)
		line = '\t\t<depth>' + str(depth) + '</depth>\n'
		voc.write(line)
		line = '\t</size>\n'
		voc.write(line)
		line = '\t<segmented>Unspecified</segmented>\n'
		voc.write(line)


def writeXML(xml_path, objname, anno):
	xmin = anno[0]
	xmax = anno[1]
	ymin = anno[2]
	ymax = anno[3]
	with open(xml_path, "a") as voc:
		line = '\t<object>\n'
		voc.write(line)
		line = '\t\t<name>' + objname + '</name>\n'
		voc.write(line)
		line = '\t\t<pose>Unspecified</pose>\n'
		voc.write(line)
		line = '\t\t<truncated>Unspecified</truncated>\n'
		voc.write(line)
		line = '\t\t<difficult>Unspecified</difficult>\n'
		voc.write(line)
		line = '\t\t<bndbox>\n'
		voc.write(line)

		# Y positive down in MOC, same as VOC.
		line = '\t\t\t<xmin>' + str(xmin) + '</xmin>\n'
		voc.write(line)
		line = '\t\t\t<ymin>' + str(ymin) + '</ymin>\n'
		voc.write(line)
		line = '\t\t\t<xmax>' + str(xmax) + '</xmax>\n'
		voc.write(line)
		line = '\t\t\t<ymax>' + str(ymax) + '</ymax>\n'
		voc.write(line)

		line = '\t\t</bndbox>\n'
		voc.write(line)
		line = '\t</object>\n'
		voc.write(line)
	return True


def FinishXML(xml_path):
	with open(xml_path, "a") as voc:
		line = '</annotation>\n'
		voc.write(line)
	return True


def writeyolabel(txt_path, dataname, box):  # YOLO用のラベル形式にする
	# print(box)
	name = box[0]
	box_x = str(round(box[1], 5))
	box_y = str(round(box[2], 2))
	box_w = str(round(box[3], 2))
	box_h = str(round(box[4], 2))
	print(dataname)
	with open(txt_path, "a") as yolo:
		yolo.write(name + " " + box_x + " " + box_y + " " + box_w + " " + box_h + "\n")  # (class x y w h)
	return True
