import modules.common_params as g
import modules.utils as utils

# If debug:
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
        model_type = g.config['edgetpu_mobilenet_ssd_type']
        if model_type == 'v1':
            model_file_abs_path = g.config['edgetpu_mobilenet_ssd_model_v1']
        else:
            model_file_abs_path = g.config['edgetpu_mobilenet_ssd_model_v2']

        if self.initialize:
            self.populate_class_labels()
            g.logger.debug('Initializing MobileNet SSD {} TFlife EdgeTPU model'.format(model_type))
            g.logger.debug('edgetpu_ssd_mobilenet_models:{}'.format(model_file_abs_path))
            
            # If debug
            start = datetime.datetime.now()
            
            self.engine = DetectionEngine(model_file_abs_path)
            
            # If debug
            diff_time = (datetime.datetime.now() - start).microseconds/1000
            g.logger.debug ('MobileNet SSD v2 EdgeTPU initialization (loading model from disk) took: {} milliseconds'.format(diff_time))

            self.initialize = False
          
        # https://coral.ai/docs/reference/edgetpu.detection.engine/#edgetpu.detection.engine.DetectionEngine.detect_with_image
        conf_threshold = g.config['edgetpu_mobilenet_ssd_min_confidence']
        detection_candidates = self.engine.detect_with_image (image, threshold=conf_threshold, keep_aspect_ratio=True, relative_coord=False, top_k=10)
        g.logger.debug ('MobileNet SSD v2 EdgeTPU detection took: {} milliseconds'.format(self.engine.get_inference_time()))
       
       # Increased speed by running only one processing loop
        detections = []
        for detected_object in detection_candidates:
            obj = {
                'type': 'object',
                'label': self.classes[detected_object.label_id],
                'confidence': "{:.2f}%".format(detected_object.score * 100),
                'box': [int(round(num)) for num in [*detected_object.bounding_box[0], *detected_object.bounding_box[1]]]
            }
            detections.append(obj)

        return detections

