from flask import Flask, render_template, Response, jsonify
import cv2
import io
from cameraClass import CameraClass

app = Flask(__name__)

cam = CameraClass()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        #TODO: Add empty bed dector. If bed empty=true, skip baby_evaluation
        camera.baby_evaluation()
        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/baby_details')
# TODO: Convert Awake/Asleep from polling to push
def baby_details():
    return jsonify(baby_state=cam.baby_state.title())

@app.route('/timestamps')
# TODO: Convert Timestamp from polling ot push
def timestamps():
    return jsonify(timestamps=cam.baby_timestamps)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)