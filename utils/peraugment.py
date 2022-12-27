from albumentations import *
import random

import cv2

def Geometric_Transformations(aug_list, cfg):
    # 简单的几何变换：反转，旋转
    
    if "flipud" in cfg:
        aug_list.append(VerticalFlip(p = cfg["flipud"]))
    
    if "fliplr" in cfg:
        aug_list.append(HorizontalFlip(p = cfg["fliplr"]))
    
    if "randomrotate" in cfg :
        theta = random.randint(-180, 180)
        aug_list.append(SafeRotate(limit=theta, p=cfg["randomrotate"]))
    
    if "rotate90" in cfg:
        
        aug_list.append(SafeRotate(limit=[90,90], border_mode = cv2.BORDER_CONSTANT, p=cfg["rotate90"]))
    if "rotate180" in cfg:
        aug_list.append(SafeRotate(limit=[180,180], p=cfg["rotate180"]))
    if "rotate270" in cfg:
        aug_list.append(SafeRotate(limit=[-90,-90], p=cfg["rotate270"]))
        
    # if "randomshiftscalerotate" in cfg and cfg["randomshiftscalerotate"] > 0:
    #     theta = random.randint(-180, 180)
    #     scale = random.uniform(0, 2)
    #     shift = random.uniform(0, 1)
    #     print(theta,scale, shift )
    #     aug_list.append(ShiftScaleRotate(shift_limit=shift, scale_limit=scale, rotate_limit=theta, p=cfg["randomshiftscalerotate"]))

def Size_Transformations(aug_list, cfg):
    if "resize" in cfg:
        aug_list.append(Resize(height=cfg["resize"][0], width=cfg["resize"][1]))
    if "longesresize" in cfg:
        aug_list.append(LongestMaxSize(max_size=cfg["longesresize"]))
    if "randomscale" in cfg:
        scale = random.uniform(0, 1)
        aug_list.append(RandomScale(scale_limit=scale, p=cfg["randomscale"]))
  
def Crop_Transformations(aug_list, cfg):  
    if "saferandomcrop" in cfg:
        # 随机裁剪 rate ，剪裁后bbox的面积比原来box减少的百分比rate
        rate = random.uniform(0, 0.3)
        aug_list.append(BBoxSafeRandomCrop(erosion_rate=rate, p=cfg["saferandomcrop"]))  
    
def HSV_Transformations(aug_list, cfg):
    
    if "randombrightness" in cfg:
        aug_list.append(RandomBrightnessContrast(brightness_limit=(0, 0.4), contrast_limit=(0, 0.4), p=cfg["randombrightness"]))
    
    if "randomhsv" in cfg:
        # 色调(H)、饱和度(S)和明度(V)
        # h = random.randint(20, 360)
        # s = random.randint(20, 360)
        # v = random.randint(20, 360)
        
        # aug_list.append(HueSaturationValue(hue_shift_limit=h,sat_shift_limit=s,val_shift_limit=v,p=cfg["randomhsv"]))
        aug_list.append(HueSaturationValue(p=cfg["randomhsv"]))
    
    if "colorjitter" in cfg:
        
        brightness = random.uniform(0.1, 1)
        contrast = random.uniform(0.1, 1)
        Saturation = random.uniform(0.1, 1)
        color = random.uniform(0.1, 1)
        aug_list.append(ColorJitter(brightness, contrast, Saturation, color, p=cfg["colorjitter"]))

    if "randomrgb" in cfg:
        r = random.randint(20, 220)
        g = random.randint(20, 220)
        b = random.randint(20, 220)
        aug_list.append(RGBShift(r_shift_limit=r,g_shift_limit=g,b_shift_limit=b,p=cfg["randomrgb"]))
 
def Perspective_Transformations(aug_list, cfg):
    if "perspective" in cfg:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        aug_list.append(Perspective(scale=(0.1,0.1), fit_output = True, pad_val=(b,g,r), p=cfg['perspective']))
    
def Blur_Transformations(aug_list, cfg):
    if "motionblur" in cfg:
        aug_list.append(MotionBlur(p=cfg['motionblur']))
        
    if "mediablur" in cfg:    
        aug_list.append(MedianBlur(blur_limit=3, p=cfg['mediablur']))
        
    if "glassblur" in cfg:    
        aug_list.append(GlassBlur(sigma=1, max_delta = 3, p=cfg['glassblur']))

def Other_Transformations(aug_list, cfg):
    if "randomsnow" in cfg:
        # 下雪
        aug_list.append(RandomSnow(p=cfg['randomsnow']))
        
    if "randomrain" in cfg:
        # 下雨
        bc = random.uniform(0.5, 0.9)
        aug_list.append(RandomRain(brightness_coefficient=bc, drop_width=1, p=cfg['randomrain']))
        
    if "randomsunflare" in cfg:
        # 逆光
        aug_list.append(RandomSunFlare(flare_roi=(0, 0, 1, 0.5), angle_lower=0.5, p=cfg['randomsunflare']))