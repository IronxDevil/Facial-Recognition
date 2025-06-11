# Facial Recognition System

A real-time facial recognition web application built with Flask, OpenCV, and DeepFace that can identify faces, detect gender, and analyze emotions from live webcam feed.

## Features

- 🎭 **Real-time Face Recognition**: Identify known faces from your database
- 👤 **Gender Detection**: Automatically detect gender (Male/Female)
- 😊 **Emotion Analysis**: Recognize emotions (Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral)
- 📹 **Live Webcam Feed**: Real-time video processing
- 🌐 **Web Interface**: User-friendly Flask web application
- 📊 **Confidence Scoring**: Shows recognition confidence percentage
- 🔄 **Dynamic Database**: Add photos and reload without restarting

## Tech Stack

- **Backend**: Python, Flask
- **Computer Vision**: OpenCV, DeepFace, Dlib
- **Frontend**: HTML5, CSS3, JavaScript
- **Machine Learning**: TensorFlow (via DeepFace)

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd facial-recognition-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
Navigate to `http://localhost:5000`

## Usage

### Setting up the Database

1. Navigate to the `database/photos/` folder
2. Add photos of people you want to recognize
3. Name the files with the person's name (e.g., `john_doe.jpg`, `jane_smith.png`)
4. Supported formats: JPG, JPEG, PNG

### Using the Application

1. **Start the Application**: Run `python app.py`
2. **Open Browser**: Go to `http://localhost:5000`
3. **Allow Camera Access**: Grant webcam permissions when prompted
4. **Add Photos**: Place photos in `database/photos/` folder
5. **Reload Database**: Click "Reload Database" after adding new photos
6. **Start Recognition**: Click "Start Recognition" to begin analysis
7. **View Results**: See real-time results for identity, gender, and emotion

## Project Structure
