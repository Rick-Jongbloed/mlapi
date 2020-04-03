#import cv2
#import numpy as np
import modules.common_params as g
import os
import modules.utils as utils
import datetime

from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils

#class ObjectTPU:
class Object:

    def __init__(self):
        self.initialize = True
        self.engine = None          # Was: self.net
        self.classes = None

    def populate_class_labels(self):
        self.classes = dataset_utils.read_label_file(g.config['edgetpu_mobilenet_ssd_labels'])           # Returns object x <todo>

    def detect(self, image):
        print (image)
        model_type = g.config['edgetpu_mobilenet_ssd_type']
        if model_type == 'v1':
            model_file_abs_path = g.config['edgetpu_mobilenet_ssd_model_v1']
        else:
            model_file_abs_path = g.config['edgetpu_mobilenet_ssd_model_v2']

        if self.initialize:
            self.populate_class_labels()
            g.logger.debug('Initializing MobileNet SSD {} TFlife EdgeTPU model'.format(model_type))
            g.logger.debug('edgetpu_ssd_mobilenet_models:{}'.format(model_file_abs_path))
            start = datetime.datetime.now()
            self.engine = DetectionEngine(model_file_abs_path)
            diff_time = (datetime.datetime.now() - start).microseconds/1000
            g.logger.debug ('MobileNet SSD v2 EdgeTPU initialization (loading model from disk) took: {} milliseconds'.format(diff_time))

            self.initialize = False
          
        # https://coral.ai/docs/reference/edgetpu.detection.engine/#edgetpu.detection.engine.DetectionEngine.detect_with_image
        #min_threshold = 0.2
        min_threshold = 0.2
        conf_threshold = g.config['edgetpu_mobilenet_ssd_min_confidence']
        
        #detection_candidates = self.engine.detect_with_image (image, threshold=min_threshold, keep_aspect_ratio=True, relative_coord=False, top_k=10)
        detection_candidates = self.engine.detect_with_image (image, threshold=0.4, keep_aspect_ratio=True, relative_coord=False, top_k=10)

        inference_time = self.engine.get_inference_time()
        g.logger.debug ('MobileNet SSD v2 EdgeTPU detection took: {} milliseconds'.format(inference_time))

        bbox = []
        label = []
        conf = []

        for detected_object in detection_candidates:
            if detected_object.score >= conf_threshold:
                bbox.append([int(round(num)) for num in [*detected_object.bounding_box[0], *detected_object.bounding_box[1]]])              # Have to see if i really need to round the numbers here, as 
                label.append(self.classes[detected_object.label_id])
                conf.append(detected_object.score)
                g.logger.info ('object:{} at {} has a acceptable confidence:{} compared to min confidence of: {}, adding'.format(label[-1], bbox[-1], conf[-1], conf_threshold))
            else:
                #g.logger.info ('rejecting object:{} at {} because its confidence is :{} compared to min confidence of: {}'.format(self.classes[detected_object.label_id]), [int(round(x)), int(round(y)), int(round(x + w)), int(round(y + h))], confidences[i], g.config['yolo_min_confidence']))
                g.logger.info ('rejecting object:{} because its confidence is :{} compared to min confidence of: {}'.format(self.classes[detected_object.label_id], detected_object.score, conf_threshold))
                
        detections = []

        for l, c, b in zip(label, conf, bbox):
            c = "{:.2f}%".format(c * 100)
            print (c)
            obj = {
                'type': 'object',
                'label': l,
                'confidence': c,
                'box': b
            }
            detections.append(obj)

        return detections

