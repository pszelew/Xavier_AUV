from flask import Flask, request, Response
import time
import pickle
import os
import argparse as ap
from neural_networks.utils.DarknetYoloModel import DarknetYoloModel
from camera_server.CameraClient import CameraClient
from utils.project_managment import PROJECT_ROOT
from definitions import IP_ADDRESS, LOG_DIRECOTRY
from logpy.LogPy import Logger

if __name__ == "__main__":
    logger = Logger(filename='darknet_server', title="Darknet_Server", directory=LOG_DIRECOTRY, logexists='append')

    parser = ap.ArgumentParser(description="Darknet yolo server")
    #parser.add_argument("-p", '--port', default=5000, type=int, help="Port on which server will be run")
    #parser.add_argument("-m", '--model', required=True, type=str, help="Path to model folder, relative to project root")
    parser.add_argument("-t", '--threshold', default=0.5, type=float, help="Detection threshold (from 0 to 1)")

    args = parser.parse_args()

    server = Flask(__name__)

    cam_client = CameraClient(host=str(os.system('hostname -I')))
    model = DarknetYoloModel(model_path=f"{PROJECT_ROOT}/neural_networks/models",
                             threshold=args.threshold)

    model.load(model_name='gate')
    logger.log("Model loaded to server")

    predict_time = 0

    @server.route("/predict_with_image", methods=["GET"])
    def predict_with_image():
        start = time.time()
        img = cam_client.frame
        getting_frame = time.time()-start
        start = time.time()
        result = model.predict(img)
        global predict_time 
        predict_time = time.time()-start
        start = time.time()
        result.append(img)
        result = pickle.dumps(result)
        packing_time = time.time()-start
        logger.log(f"INFO: prediction time: " + str(round(predict_time, 4)) + " getting frame time: " +
                   str(round(getting_frame, 4)) + " message append and picke: " + str(round(packing_time, 4)) +
                   " sum:" + str(round(predict_time+getting_frame + packing_time, 4)))
        return result

    @server.route("/predict", methods=["GET"])
    def predict():
        img = cam_client.frame
        start = time.time()
        logger.log("Starting prediction")
        result = model.predict(img)
        global predict_time 
        predict_time = time.time()-start
        logger.log(f"INFO: prediction time: " + str(predict_time))
        return pickle.dumps(result)

    @server.route("/is_ready", methods=["GET"])
    def is_ready():
        return 'true'

    @server.route("/prediction_time", methods=["GET"])
    def prediction_time():
        global predict_time
        return str(predict_time)

    @server.route("/change_threshold", methods=["POST"])
    def change_threshold():
        thresh = request.args.get('threshold', default='0.5', type=float)
        model.threshold = thresh
        return 'true'

    @server.route("/load_model", methods=["POST"])
    def load_model():
        model_path = request.args.get('model_name', default='*', type=str)
        logger.log(f"INFO: loading new model: {model_path}")
        model.load(model_path)
        # TODO
        # add return false if operation failsed 
        return 'true'


    @server.route("/change_camera", methods=["POST"])
    def change_camera():
        cam = request.args.get('cam_name', default='front', type=str)
        logger.log(f"INFO: changing camera new cam id: {cam}")
        # camera change method returns 'true' if succed, 'false' otherwise
        return cam_client.change_camera(cam)
        
    logger.log("Server host "+IP_ADDRESS)
    with open('ports.txt','r') as f:
        Darknet_port = int(f.read())+2
    print("Serwer darknet port",str(Darknet_port))
    server.run(host=IP_ADDRESS, port=Darknet_port)
    logger.log("Server runs")
