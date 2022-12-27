# augment

pip install -r requirement.txt   
python demo_label_file.py


- name 总的标签list
name = ['person' ]   

- select_aug_dict 选择的数据增强方式，每种方式都是独立的，详情见 config/test.yaml   
select_aug_dict = { 'flipud', 'fliplr', 'randomrotate', 
                       'rotateleft90', 'rotateleft180', 'rotateleft270',
                        'randomscale', 'saferandomcrop',
                        'randombrightness', 'randomhsv', 'colorjitter', 'randomrgb',
                        'perspective',
                        'motionblur', 'mediablur', 'glassblur',
                        'randomsnow', 'randomrain', 'randomsunflare'}     

- 只针对select_label里的标签进行augment，不在这里面的，不做augment，并且保存的xml也只包含select_label的标签   
- select_label的范围 <= name list   
select_label = {'bj', 'bj_bpmh', 'bj_bpps', 'bj_wkps', 'bjdsyc',
    'byq_hxq', 'hxq_gjbs','hxq_gjtps', 'ywzt_yfyc', 'ywzt_yfzc',
    'yw_gkxfw', 'yw_nc', 'gbps', 'sly_dmyw', 'jyz_pl',
    'xmbhzc', 'xmbhyc', 'kgg_ybh', 'kgg_ybf','kgg_wyb',
    'person', 'aqmzc', 'wcaqm', 'wcgz', 'gzzc', 'hand', 'hand_xy', 'xy'}   
 