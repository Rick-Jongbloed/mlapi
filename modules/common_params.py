import modules.log as g_log



MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])
ACCESS_TOKEN_EXPIRES = 60 * 60  # 1 hr

log = g_log.Log()
logger = log;

config = {}
config_vals = {
         'secrets':{
            'section': 'general',
            'default': None,
            'type': 'string',
        },
        'processes':{
            'section': 'general',
            'default': '1',
            'type': 'int',
        },
        'port':{
            'section': 'general',
            'default': '5000',
            'type': 'int',
        },
        'images_path':{
            'section': 'general',
            'default': './images',
            'type': 'string',
        },
        'db_path':{
            'section': 'general',
            'default': './db',
            'type': 'string',
        },
        'mlapi_secret_key':{
            'section': 'general',
            'default': None,
            'type': 'string',
        },

        # General ML
        'use_opencv_dnn_cuda':{
            'section':'ml',
            'default':'no',
            'type':'string'
        },
        'use_tflite_edgetpu':{
            'section':'ml',
            'default':'no',
            'type':'string'
        },
        # YOLO
        'yolo_type':{
            'section':'yolo',
            'default':'full',
            'type':'string'
        },
        'yolo_min_confidence': {
            'section': 'yolo',
            'default': '0.4',
            'type': 'float'
        },
        'config':{
            'section': 'yolo',
            'default': './models/yolov3/yolov3.cfg',
            'type': 'string'
        },
        'weights':{
            'section': 'yolo',
            'default': './models/yolov3/yolov3.weights',
            'type': 'string'
        },
        'labels':{
            'section': 'yolo',
            'default': './models/yolov3/yolov3_classes.txt',
            'type': 'string'
        },
        'tiny_config':{
            'section': 'yolo',
            'default': './models/tinyyolo/yolov3-tiny.cfg',
            'type': 'string'
        },
        'tiny_weights':{
            'section': 'yolo',
            'default': './models/tinyyolo/yolov3-tiny.weights',
            'type': 'string'
        },
        'tiny_labels':{
            'section': 'yolo',
            'default': './models/tinyyolo/yolov3-tiny.txt',
            'type': 'string'
        },
        # EdgeTPU SSD Mobilenet
        'edgetpu_mobilenet_ssd_type':{
            'section':'edgetpu_mobilenet_ssd',
            'default':'v2',
            'type':'string'
        },
        'edgetpu_mobilenet_ssd_min_confidence': {
            'section': 'yolo',
            'default': '0.4',
            'type': 'float'
        },
        'edgetpu_mobilenet_ssd_labels':{
            'section': 'edgetpu_mobilenet_ssd',
            'default': './models/mobilenet-ssd-edgetpu/coco_labels.txt',
            'type': 'string'
        },
        'edgetpu_mobilenet_ssd_model_v1':{
            'section': 'edgetpu_mobilenet_ssd',
            'default': './models/mobilenet-ssd-edgetpu/ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite',
            'type': 'string'
        },
        'edgetpu_mobilenet_ssd_model_v2':{
            'section': 'edgetpu_mobilenet_ssd',
            'default': './models/mobilenet-ssd-edgetpu/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite',
            'type': 'string'
        },
        # Face
        'face_num_jitters':{
            'section': 'face',
            'default': '0',
            'type': 'int',
        },
        'face_upsample_times':{
            'section': 'face',
            'default': '1',
            'type': 'int',
        },
        'face_model':{
            'section': 'face',
            'default': 'hog',
            'type': 'string',
        },
        'face_train_model':{
            'section': 'face',
            'default': 'hog',
            'type': 'string',
        },
         'face_recog_dist_threshold': {
            'section': 'face',
            'default': '0.6',
            'type': 'float'
        },
        'face_recog_knn_algo': {
            'section': 'face',
            'default': 'ball_tree',
            'type': 'string'
        },
        'known_faces_path':{
            'section': 'face',
            'default': './known_faces',
            'type': 'string',
        },
        'unknown_faces_path':{
            'section': 'face',
            'default': './unknown_faces',
            'type': 'string',
        },
        'unknown_face_name':{
            'section': 'face',
            'default': 'unknown face',
            'type': 'string',
        },
         'save_unknown_faces':{
            'section': 'face',
            'default': 'yes',
            'type': 'string',
        },

        'save_unknown_faces_leeway_pixels':{
            'section': 'face',
            'default': '50',
            'type': 'int',
        },

}

