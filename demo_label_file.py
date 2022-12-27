"""
按标签在文件夹里挑选图片进行数据增强
"""
import os
from utils.augment import Get_Augment

name = [ 'bj', 'bj_bpmh', 'bj_bpps', 'bj_wkps', 'bjdsyc',
    'byq_hxq', 'hxq_gjbs','hxq_gjtps', 'ywzt_yfyc', 'ywzt_yfzc',
    'yw_gkxfw', 'yw_nc', 'gbps', 'sly_dmyw', 'jyz_pl',
    'xmbhzc', 'xmbhyc', 'kgg_ybh', 'kgg_ybf','kgg_wyb',
    'person', 'aqmzc', 'wcaqm', 'wcgz', 'gzzc', 'hand', 'hand_xy', 'xy' ]

def get_start(name=name):
    name_dict = {}
    name_id = {}
    for i in range(len(name)):
        name_dict[name[i]] = i
        name_id[i] = name[i]
        # name_dict = {'bj':0, 'bjdsyc': 1}
        # name_id = {0: 'bj', 1: 'bjdsyc'}
    return name_dict, name_id

if __name__ == "__main__":
    name_dict, name_id = get_start()
    
    # imageroot = '18_cls/datasets/JPEGImages/'
    # annoroot = '18_cls/datasets/Annotations/'
    imageroot = 'data/JPEGImages/'
    annoroot = 'data/Annotations/'
    saveroot = 'save/'

    select_aug_dict = { 'flipud', 'fliplr', 'randomrotate', 
                       'rotateleft90', 'rotateleft180', 'rotateleft270',
                        'randomscale', 'saferandomcrop',
                        'randombrightness', 'randomhsv', 'colorjitter', 'randomrgb',
                        'perspective',
                        'motionblur', 'mediablur', 'glassblur',
                        'randomsnow', 'randomrain', 'randomsunflare'}

    select_label = {'bj', 'bj_bpmh', 'bj_bpps', 'bj_wkps', 'bjdsyc',
    'byq_hxq', 'hxq_gjbs','hxq_gjtps', 'ywzt_yfyc', 'ywzt_yfzc',
    'yw_gkxfw', 'yw_nc', 'gbps', 'sly_dmyw', 'jyz_pl',
    'xmbhzc', 'xmbhyc', 'kgg_ybh', 'kgg_ybf','kgg_wyb',
    'person', 'aqmzc', 'wcaqm', 'wcgz', 'gzzc', 'hand', 'hand_xy', 'xy'}
    for aug_type in select_aug_dict:
        # 初始化
        cfg = {
                    'names': name_dict, 
                    'category_id_to_name': name_id
                }
        if isinstance(aug_type, tuple):
            savename = ''
            for a in aug_type:
                cfg[a] = 1
                if savename != '':
                    savename +='_'
                savename += a
                
            savepath = os.path.join(saveroot, savename)
        else:
            cfg[aug_type] = 1
            
            savepath = os.path.join(saveroot, aug_type)
        # print("old", cfg)
        aug = Get_Augment(cfg, savepath)
        imagelist = sorted(os.listdir(imageroot))
        
        for imagename in imagelist:
            imagepath = os.path.join(imageroot, imagename)
            annopath = os.path.join(annoroot, imagename.split('.j')[0] + '.xml')
            # print(imagepath)
            # print(annopath)
            flag = aug.get_augment(imagepath, annopath, select_label = select_label)
            flag = aug.get_rotate_augment(imagepath, annopath, select_label = select_label)
            
            saveimagepath = os.path.join(savepath, imagename)
            saveannopath = os.path.join(savepath, imagename.split('.j')[0] + '.xml')
            if flag and os.path.exists(saveimagepath):
                
                aug.get_vis(saveimagepath, saveannopath)