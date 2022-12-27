import yaml
import cv2, os

from albumentations import *
from utils.utils import visualize_one_image, xmlinfo, writexml
from utils.peraugment import *
from utils.cvaugment import *

class Get_Augment():
    def __init__(self, cfg, saveroot = './save/'):
        if isinstance(cfg, dict):
            self.cfg = cfg
        else:
            with open(cfg, 'r', encoding='utf-8') as f:
                self.cfg = yaml.load(f.read(), Loader=yaml.FullLoader)
        # print(self.cfg)
        self.cls_dict = self.cfg['names']
        
        self.category_id_to_name = self.cfg['category_id_to_name']
        
        self.aug_list = []
        self.load_augment()
        # print(self.augment)
        self.saveroot = saveroot
        if not os.path.exists(self.saveroot):
            os.makedirs(self.saveroot)
    
    def load_augment(self, min_area=0., min_visibility=0.):
        
        Geometric_Transformations(self.aug_list, self.cfg)
        Size_Transformations(self.aug_list, self.cfg)
        
        Crop_Transformations(self.aug_list, self.cfg)
        
        Perspective_Transformations(self.aug_list, self.cfg)
        HSV_Transformations(self.aug_list, self.cfg)
        Blur_Transformations(self.aug_list, self.cfg)
        Other_Transformations(self.aug_list, self.cfg)
        
        self.augment = Compose(self.aug_list, bbox_params=BboxParams(format='pascal_voc', min_area=min_area,
                                               min_visibility=min_visibility, label_fields=['category_id']))

    def get_prepare(self, imagepath, annopath, select_label = ''):
        image = cv2.imread(imagepath)
        w = image.shape[1]
        h = image.shape[0]
        self.cfg['w'] = w
        self.cfg['h'] = h
        bboxes, cls_id, flag = xmlinfo(self.cfg, annopath, cls_dict=self.cls_dict, select_label = select_label)
        
        if flag:
            annotations = {'image': image, 
                        'bboxes': bboxes,
                        'category_id': cls_id
                        }
            
            return annotations
        else:
            return 0
    
    def get_augment(self, imagepath, annopath, select_label = ''):
        
        imagename = imagepath.split('/')[-1].split('.j')[0]
        
        annotations = self.get_prepare(imagepath, annopath, select_label)
        
        if annotations == 0:
            print('***warning:', imagepath, 'have nochange images,continue!')
            # cv2.imwrite(saveimagepath, augmented['image'])
            return 0
        # visualize_one_image(annotations, self.category_id_to_name)
        # print(annotations, self.augment)
        augmented = self.augment(**annotations)
        
        # visualize_one_image(augmented, self.category_id_to_name)
        
        # print(augmented)
        saveimagepath = os.path.join(self.saveroot, imagename + '.jpg')
        saveannopath = os.path.join(self.saveroot, imagename + '.xml')
        
        cv2.imwrite(saveimagepath, augmented['image'])
        writexml(augmented['bboxes'], augmented['category_id'], augmented['image'], self.category_id_to_name, saveimagepath, saveannopath)

        return 1
    
    def get_rotate_augment(self, imagepath, annopath, select_label = ''):
        imagename = imagepath.split('/')[-1].split('.j')[0]
        annotations = self.get_prepare(imagepath, annopath, select_label)
        # print(annotations)
        if annotations == 0:
            print('***warning:', imagepath, 'have nochange images,continue!')
            # cv2.imwrite(saveimagepath, augmented['image'])
            return 0
        augmented = CV_Rotate_Transformations(annotations, self.cfg)
        
        saveimagepath = os.path.join(self.saveroot, imagename + '.jpg')
        saveannopath = os.path.join(self.saveroot, imagename + '.xml')

        cv2.imwrite(saveimagepath, augmented['image'])
        writexml(augmented['bboxes'], augmented['category_id'], augmented['image'], self.category_id_to_name, saveimagepath, saveannopath)

    def get_vis(self, imagepath, annopath, savepath = './test.jpg'):
        annotations = self.get_prepare(imagepath, annopath)
        visualize_one_image(annotations, self.category_id_to_name, savepath)