# 用于图片上的边界框和类别 labels 的可视化函数
BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

import cv2 
import xml.etree.ElementTree as ET
import pascal_voc_writer as voc

def visualize_bbox(img, bbox, class_id, class_idx_to_name, color=BOX_COLOR, thickness=2):
    x_min, y_min, x_max, y_max = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    class_name = class_idx_to_name[class_id]
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(img, class_name, (x_min, y_min - int(0.3 * text_height)), cv2.FONT_HERSHEY_SIMPLEX, 0.35,TEXT_COLOR, lineType=cv2.LINE_AA)
    return img

def visualize_one_image(annotations, category_id_to_name, savepath = './test.jpg'):
    img = annotations['image'].copy()
    for idx, bbox in enumerate(annotations['bboxes']):
        img = visualize_bbox(img, bbox, annotations['category_id'][idx], category_id_to_name)
    cv2.imwrite(savepath, img)


def xmlinfo(cfg, annpath, cls_dict, select_label = ''):
    bboxes = []
    cls_id = []
    
    w = cfg['w']
    h = cfg['h']
    tree=ET.parse(annpath)
    root = tree.getroot()
    
    objects= root.findall('object')
    
    flag = False
    if select_label == '':
        flag = True
    
    for obj in objects:
        name = obj[0].text
        xmlbox = obj.find('bndbox')
        #print(xmlbox)
        xmin = max(0, int(float(xmlbox[0].text)))     
        xmax = min(w, int(float(xmlbox[2].text)))
        ymin = max(0, int(float(xmlbox[1].text)))
        ymax = min(h, int(float(xmlbox[3].text)))
            
        if name in select_label:
            flag = True
        if name == 'hxq_gjtbs':
            cfg['randomrgb'] = 0
            cfg['randomhsv'] = 0
            
        bbox = [xmin, ymin, xmax, ymax]
        bboxes.append(bbox)
        cls_id.append(cls_dict[name])
    return bboxes, cls_id, flag

def writexml(bboxes, cls_id, image, cls_dict, imagepath, annopath):
    writer = voc.Writer(imagepath, image.shape[1], image.shape[0])  # 图片完整路径和图片像素大小 w,h
    # print(len(bboxes))
    for bbox_id in range(len(bboxes)): 
        bbox = bboxes[bbox_id]
        cls = cls_dict[cls_id[bbox_id]]
        writer.addObject(name=cls, xmin = bbox[0], xmax = bbox[2], ymin = bbox[1], ymax = bbox[3])  # 写入
        writer.save(annopath) # 保存
    print("文件{}创建完成".format(annopath))