from flask import Flask, render_template, Response, jsonify
import cv2
import os
import numpy as np
from deepface import DeepFace
import json
from datetime import datetime
import threading
import time
import tensorflow as tf

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'database/photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Global variables
camera = None
recognition_active = False
current_results = {
    'identity': 'Unknown',
    'gender': 'Unknown',
    'emotion': 'Unknown',
    'confidence': 0
}

class FacialRecognitionSystem:
    def __init__(self, database_path):
        self.database_path = database_path
        self.known_faces = []
        self.face_cascade = None
        self.initialize_opencv()
        self.load_database()
    
    def initialize_opencv(self):
        """Initialize OpenCV face cascade"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            if self.face_cascade.empty():
                print("❌ Failed to load face cascade")
            else:
                print("✅ OpenCV face cascade loaded")
        except Exception as e:
            print(f"❌ OpenCV initialization error: {e}")
    
    def load_database(self):
        """Load all images from the database folder"""
        self.known_faces = []
        try:
            if not os.path.exists(self.database_path):
                os.makedirs(self.database_path, exist_ok=True)
                print(f"📁 Created database folder: {self.database_path}")
            
            for filename in os.listdir(self.database_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filepath = os.path.join(self.database_path, filename)
                    name = os.path.splitext(filename)[0]
                    self.known_faces.append({
                        'name': name,
                        'path': filepath
                    })
            print(f"📸 Loaded {len(self.known_faces)} faces from database")
        except Exception as e:
            print(f"❌ Database loading error: {e}")
    
    def recognize_face(self, frame):
        """Recognize face and analyze gender and emotion"""
        global current_results
        
        try:
            # Analyze the frame for face recognition, gender, and emotion
            analysis = DeepFace.analyze(
                frame, 
                actions=['gender', 'emotion'],
                enforce_detection=False,
                silent=True
            )
            
            # Handle both single face and multiple faces
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            # Extract gender and emotion
            gender = analysis.get('dominant_gender', 'Unknown')
            emotion = analysis.get('dominant_emotion', 'Unknown')
            
            # Try to find matching face in database
            identity = 'Unknown'
            confidence = 0
            
            if len(self.known_faces) > 0:
                try:
                    # Compare with database faces
                    for known_face in self.known_faces:
                        try:
                            result = DeepFace.verify(
                                frame, 
                                known_face['path'],
                                enforce_detection=False,
                                silent=True
                            )
                            
                            if result['verified']:
                                identity = known_face['name']
                                confidence = (1 - result['distance']) * 100
                                break
                        except Exception as verify_error:
                            continue
                except Exception as recognition_error:
                    print(f"Recognition error: {recognition_error}")
            
            current_results = {
                'identity': identity,
                'gender': gender,
                'emotion': emotion,
                'confidence': round(confidence, 2)
            }
            
        except Exception as e:
            print(f"Analysis error: {e}")
            current_results = {
                'identity': 'Unknown',
                'gender': 'Unknown',
                'emotion': 'Unknown',
                'confidence': 0
            }

# Initialize the facial recognition system
try:
    fr_system = FacialRecognitionSystem(UPLOAD_FOLDER)
    print("✅ Facial Recognition System initialized")
except Exception as e:
    print(f"❌ System initialization error: {e}")
    fr_system = None

def generate_frames():
    """Generate frames from webcam with face detection"""
    global camera, recognition_active
    
    try:
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("❌ Cannot open camera")
            return
        
        print("📹 Camera opened successfully")
        
        while True:
            success, frame = camera.read()
            if not success:
                print("❌ Failed to read frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect faces using OpenCV
            if fr_system and fr_system.face_cascade:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = fr_system.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                # Draw rectangles around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    # Add recognition results text
                    if recognition_active:
                        cv2.putText(frame, f"Identity: {current_results['identity']}", 
                                   (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        cv2.putText(frame, f"Gender: {current_results['gender']}", 
                                   (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        cv2.putText(frame, f"Emotion: {current_results['emotion']}", 
                                   (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        if current_results['confidence'] > 0:
                            cv2.putText(frame, f"Confidence: {current_results['confidence']}%", 
                                       (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Perform recognition analysis in a separate thread to avoid blocking
                if recognition_active and len(faces) > 0 and fr_system:
                    threading.Thread(target=fr_system.recognize_face, args=(frame,), daemon=True).start()
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
    except Exception as e:
        print(f"❌ Frame generation error: {e}")
    finally:
        if camera:
            camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recognition')
def start_recognition():
    global recognition_active
    try:
        recognition_active = True
        if fr_system:
            fr_system.load_database()  # Reload database
        return jsonify({'status': 'Recognition started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop_recognition')
def stop_recognition():
    global recognition_active
    try:
        recognition_active = False
        return jsonify({'status': 'Recognition stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_results')
def get_results():
    return jsonify(current_results)

@app.route('/reload_database')
def reload_database():
    try:
        if fr_system:
            fr_system.load_database()
            return jsonify({'status': f'Database reloaded. {len(fr_system.known_faces)} faces loaded.'})
        else:
            return jsonify({'error': 'System not initialized'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print("\n🚀 Starting Facial Recognition System...")
    print("📱 Open your browser and go to: http://localhost:5000")
    
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5050)