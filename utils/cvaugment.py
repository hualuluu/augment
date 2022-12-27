import cv2
def CV_Rotate_Transformations(annotations, cfg):  
    if "rotateleft90" in cfg and cfg["rotateleft90"]:
        annotations['image'] = cv2.rotate(annotations['image'], cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        new_bbox = []
        for b in annotations['bboxes']:
            xmin, ymin, xmax, ymax = b
            
            new_xmin = ymin
            new_ymin = (cfg['w'] - xmax)
            new_xmax = ymax
            new_ymax = (cfg['w'] - xmin)
            new_bbox.append([new_xmin, new_ymin, new_xmax, new_ymax])
        annotations['bboxes'] = new_bbox
        cfg['w'], cfg['h'] = cfg['h'], cfg['w']
        
    if "rotateleft180" in cfg and cfg["rotateleft180"]:
        annotations['image'] = cv2.rotate(annotations['image'], cv2.ROTATE_180)
        
        new_bbox = []
        for b in annotations['bboxes']:
            xmin, ymin, xmax, ymax = b
            
            new_xmin = (cfg['w'] - xmax)
            new_ymin = cfg['h'] - ymax
            new_xmax = (cfg['w'] - xmin)
            new_ymax = cfg['h'] - ymin
            new_bbox.append([new_xmin, new_ymin, new_xmax, new_ymax])
        annotations['bboxes'] = new_bbox
        
    if "rotateleft270" in cfg and cfg["rotateleft270"]:
        annotations['image'] = cv2.rotate(annotations['image'], cv2.ROTATE_90_CLOCKWISE)
        
        new_bbox = []
        for b in annotations['bboxes']:
            xmin, ymin, xmax, ymax = b
            
            new_xmin = cfg['h'] - ymax
            new_ymin = xmin
            new_xmax = cfg['h'] - ymin
            new_ymax = xmax
            new_bbox.append([new_xmin, new_ymin, new_xmax, new_ymax])
        annotations['bboxes'] = new_bbox
        cfg['w'], cfg['h'] = cfg['h'], cfg['w']
        
    return annotations
      