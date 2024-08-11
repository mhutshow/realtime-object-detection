import random
from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import torch
from threading import Lock

app = Flask(__name__)
CORS(app)  

# Load  model
model = torch.hub.load('/Users/mahedihasan/Desktop/detection/ai_model_with_flask_api/', 'yolov5s', source='local')

detected_objects = []
lock = Lock()

# color mapping for specific object classes
COLOR_MAPPING = {
    'person': (255, 0, 0),      # Blue
    'car': (255, 20, 147),      # Pink
    'bicycle': (0, 255, 0),     # Green
    'dog': (0, 255, 255),       # Cyan
    'cat': (255, 255, 0),       # Yellow
    'chair': (128, 0, 128),     # Purple
}

def get_color_for_label(label):
    """Return the color for a specific label, or generate a random color if not specified."""
    if label in COLOR_MAPPING:
        return COLOR_MAPPING[label]
    else:
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color

def generate_frames():
    global detected_objects
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Frame capture failed.")
            break

        try:
            # YOLOv5 detection on the frame
            results = model(frame)
        except Exception as e:
            print(f"Error during model inference: {e}")
            continue

        temp_detected_objects = []
        try:
            for det in results.xyxy[0]:
                x1, y1, x2, y2, conf, cls = det
                label = model.names[int(cls)]
                color = get_color_for_label(label)  
                temp_detected_objects.append((label, conf)) 

                
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        except Exception as e:
            print(f"Error during detection processing: {e}")

    
        with lock:
            detected_objects = temp_detected_objects

        
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Frame encoding failed.")
                continue
            frame = buffer.tobytes()
        except Exception as e:
            print(f"Error during frame encoding: {e}")
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detection_results')
def detection_results():
    global detected_objects

    
    detection_summary = {}
    with lock:
        for obj in detected_objects:
            label, conf = obj  
            conf = float(conf)
            if label in detection_summary:
                detection_summary[label]['count'] += 1
                detection_summary[label]['scores'].append(conf)
            else:
                detection_summary[label] = {'count': 1, 'scores': [conf]}

    
    for label in detection_summary:
        scores = detection_summary[label]['scores']
        detection_summary[label]['average_score'] = sum(scores) / len(scores)

    
    formatted_summary = {f"{label} (avg score: {detection_summary[label]['average_score']:.2f})": detection_summary[label]['count'] for label in detection_summary}

    return jsonify(formatted_summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
