# **Realtime Object Detection from Live Camera**

## **Overview**

This project provides a real-time object detection solution using a powerful, custom-trained deep learning model based on YOLOv5. The backend, powered by Flask, handles video processing and model inference, while the frontend, built with React, displays the live video stream along with detected objects. Each detected object is highlighted with a color-coded bounding box and label, enhancing visual distinction.

## **Video Preview**

[Watch the video preview here](https://www.youtube.com/watch?v=hmsWj5Ewhwg)


## **Project Structure**

- **`ai_model_with_flask_api/`**: Contains the Conda environment, the custom-trained YOLOv5 model, and Flask API for backend processing.
- **`react_frontend/`**: Contains the React frontend that displays the live video stream and detected objects.

## **Features**

- **Real-Time Object Detection**: Processes live video feed with a custom-trained deep learning model to detect and label objects in real-time.
- **Color-Coded Detection**: Each detected object is highlighted with a unique color, even if they are of the same type.
- **Responsive UI**: The React frontend is responsive, providing a clean and user-friendly interface.

## **Technologies Used**

- **Backend**: Flask, OpenCV, PyTorch, Custom-Trained YOLOv5 Model
- **Frontend**: React, JavaScript, HTML, CSS

## **Getting Started**

### **Prerequisites**

To run this project locally, ensure you have the following installed:

- Conda (for environment management)
- Node.js 14+
- npm (Node Package Manager)

### **Installation**

#### **1. Clone the Repository**

```bash
git clone https://github.com/mhutshow/realtime-object-detection-live-camera.git
cd realtime-object-detection-live-camera
```

#### **2. Setup the Backend**

Navigate to the `ai_model_with_flask_api` directory and set up the Conda environment:

```bash
cd ai_model_with_flask_api
conda create -n object_env python=3.8  # Create the environment (if not already created)
conda activate object_env  # Activate the environment
```

Manually install Flask and Flask-CORS, as they are not included in the environment by default:

```bash
pip install flask flask-cors
```

Ensure all other required Python packages are installed:

```bash
pip install -r requirements.txt
```

#### **3. Setup the Frontend**

Navigate to the `react_frontend` directory:

```bash
cd ../react_frontend
npm install
```

### **Running the Application**

#### **1. Start the Flask Backend**

Navigate to the `ai_model_with_flask_api` directory, activate the Conda environment if it's not already activated, and modify the model loading line in `app.py` to reflect the correct path:

```python
model = torch.hub.load('/Users/mahedihasan/Desktop/detection/ai_model_with_flask_api/', 'nameOfTheFile', source='local')
```

- Note that in the project directory, you will find other trained models based on YOLOv5. Change the model name to use a different model or your custom-trained model.

After modifying the path, run the Flask server:

```bash
cd ../ai_model_with_flask_api
conda activate object_env  # Ensure the environment is activated
python app.py
```

The Flask server will start on `http://localhost:5001`.

#### **2. Start the React Frontend**

Navigate to the `react_frontend` directory and start the React development server:

```bash
cd ../react_frontend
npm start
```

The React frontend will be available on `http://localhost:3000`.

## **Backend (Flask API) Overview**

The backend is responsible for handling the video feed, running object detection using a custom-trained deep learning model (based on YOLOv5), and providing the results to the frontend.

### **Key Responsibilities:**

- **Video Capture**: Captures frames from a live video feed using OpenCV (`cv2.VideoCapture(0)`). The video feed is usually from a connected camera, such as a webcam.

- **Object Detection**: For each captured frame, the backend uses a custom-trained YOLOv5 model to detect objects. The model predicts bounding boxes, class labels, and confidence scores for each detected object.

- **Bounding Box and Label Drawing**: The backend draws bounding boxes around detected objects in each frame, using specific colors assigned to different object classes (e.g., blue for "person", pink for "car"). For object classes not pre-defined, a random color is generated.

- **Frame Encoding**: Once the bounding boxes and labels are drawn, the frame is encoded into JPEG format and prepared for streaming to the frontend.

- **Streaming Video to Frontend**: The backend streams the processed video frames to the frontend via the `/video_feed` endpoint. This is achieved using Flask’s `Response` object, which streams the frames as a multipart response.

- **Providing Detection Results**: The backend maintains a list of detected objects, including their labels and confidence scores. This data is served to the frontend through the `/detection_results` endpoint, which returns a JSON object containing the detection results.

- **Concurrency Management**: To handle concurrent access to the detected objects list, a threading lock (`Lock()`) is used, ensuring that the list is updated in a thread-safe manner.

## **Frontend (React) Overview**

The React frontend is responsible for providing a user interface that displays the live video stream along with the detected objects.

### **Key Responsibilities:**

- **Fetching Video Feed**: Continuously fetches the live video feed from the Flask backend by rendering an `<img>` element whose `src` attribute points to the `/video_feed` endpoint. The image updates automatically as new frames are streamed from the backend.

- **Fetching Detection Results**: Periodically (every second) sends a request to the `/detection_results` endpoint to retrieve the latest detection results. These results include the labels and confidence scores of the detected objects, which are then displayed in a list format.

- **Displaying Date, Time, and Location**: Displays the current date, time, and the user’s geographical coordinates. This information is updated in real-time, with the date and time fetched locally and the location fetched using the browser’s geolocation API.

- **Updating UI with Detection Results**: Updates the UI with the latest video frame and detection results. This process repeats continuously, creating a seamless real-time object detection experience.

### **Interaction Between Backend and Frontend**

The interaction between the Flask backend and React frontend follows a structured flow:

1. **Video Stream Request**: The React frontend requests the video stream from the Flask backend via the `/video_feed` endpoint. The backend captures frames from the camera, processes them, and streams them back to the frontend in real-time.

2. **Object Detection Results Request**: Concurrently, the React frontend periodically requests object detection results from the Flask backend via the `/detection_results` endpoint. The backend responds with a JSON object containing the detection data, which is then used to update the UI.

3. **UI Update**: The frontend updates the UI with the latest video frame and detection results. This process repeats continuously, providing users with an up-to-date display of the detected objects.

### **Usage**

- **Live Stream**: Access the live video stream at `http://localhost:3000`. The stream displays real-time object detection with color-coded bounding boxes and labels.
- **Detected Objects**: Below the video stream, a list of detected objects with their counts will be displayed.

### **Customization**

- **Change Detection Model**: Modify the model used by adjusting the model loading line in `app.py` within the `ai_model_with_flask_api` directory:

  ```python
  model = torch.hub.load('path_to_model', 'medium', source='local')
  ```

- **Adjust Detection Interval**: Change the detection interval by adjusting the `setInterval` timing in the React component (`App.js`):

  ```javascript
  useEffect(() => {
    const intervalId = setInterval(() => {
      // Fetch detection results
    }, 1000); // Change interval timing here
  }, []);
  ```

- **Modify Bounding Box Colors**: To change how colors are assigned to detected objects, modify the `get_random_color()` function in `app.py`:

  ```python
  def get_random_color():
      return (r, g, b)  # Replace with specific color values
  ```

### **Troubleshooting**

- **CORS Issues**: Ensure `flask-cors` is correctly configured in `app.py` to handle cross-origin requests:

  ```python
  from flask_cors import CORS
  CORS(app)
  ```

- **Model Not Loading**: Verify that the deep learning model and dependencies are correctly installed. Check the paths and ensure the model directory is properly referenced.

- **Performance Issues**: If the application is slow, consider using a lighter model, reducing the detection interval, or resizing the input frames.

### **Contributing**

Contributions are welcome! Please fork this repository, create a feature branch, and submit a pull request. Ensure that your code adheres to the project’s coding standards and includes appropriate tests.

### **Acknowledgment**

This project leverages the YOLOv5 model architecture, developed and maintained by Ultralytics. We acknowledge and appreciate their significant contributions to the computer vision community.

### **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
