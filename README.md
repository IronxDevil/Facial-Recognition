# Facial Recognition System

A real-time web-based facial recognition system built with Python Flask, DeepFace, OpenCV, and TensorFlow. Features live face recognition, emotion analysis, gender detection, and a modern responsive web interface.

## Features

### Real-Time Recognition
- **Live Camera Feed**: Real-time facial recognition from webcam with mirror effect
- **Identity Detection**: Recognize known faces from photo database
- **Gender Detection**: Automatic gender classification (Male/Female)
- **Emotion Analysis**: Real-time emotion detection with 7 emotions
- **Confidence Scoring**: Accuracy percentage for face recognition
- **Face Detection**: OpenCV-powered face detection with bounding boxes

### Photo Management
- **Simple Database**: Store face photos in `database/photos/` folder
- **Auto-reload**: Reload database without restarting application
- **Multiple Formats**: Support for PNG, JPG, JPEG images
- **Name-based Recognition**: File names become identity labels

### Modern Interface
- **Responsive Design**: Clean, modern web interface
- **Real-time Updates**: Live recognition results display
- **Visual Status**: Active/inactive indicators with color coding
- **Control Buttons**: Start, stop, and reload functionality
- **Keyboard Shortcuts**: Quick access to main functions

### Command Buttons
- **Start Recognition**: Click start button or use interface
- **Stop Recognition**: Click stop button or use interface
- **Reload Database**: Click reload button to refresh face database

## Quick Start

### Prerequisites
- Python 3.7+
- Webcam/Camera
- Modern web browser
- At least 4GB RAM (for TensorFlow models)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/IronxDevil/Facial-Recognition.git
cd Facial-Recognition
```

2. **Run the automated installation script**
```bash
python install.py
```

The installation script will:
- Upgrade pip to latest version
- Clean any existing TensorFlow installations
- Install all required dependencies
- Test the installation
- Verify all components work correctly

3. **Manual installation (alternative)**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5050
```

## Dependencies

### Core Libraries
```txt
tensorflow==2.13.0        # Deep learning backend
keras==2.13.1             # Neural network API
deepface==0.0.79          # Face recognition & analysis
opencv-python==4.8.1.78   # Computer vision
Flask==2.3.3              # Web framework
```

### Supporting Libraries
```txt
numpy==1.24.3             # Numerical computing
Pillow==10.0.1            # Image processing
pandas==1.5.3             # Data manipulation
gdown==4.7.1              # Model downloads
tqdm==4.65.0              # Progress bars
protobuf==3.20.3          # Protocol buffers
werkzeug==2.3.7           # WSGI utilities
jinja2==3.1.2             # Template engine
```

## Project Structure

```
Facial-Recognition/
├── app.py                    # 🚀 Main Flask application
├── requirements.txt          # 📦 Python dependencies
├── install.py               # ⚙️ Automated installation script
├── README.md                # 📖 Project documentation
├── templates/
│   └── index.html           # 🌐 Main web interface
├── static/
│   ├── css/
│   │   └── style.css        # 🎨 Stylesheet (auto-generated)
│   └── js/
│       └── script.js        # ⚡ JavaScript functionality (auto-generated)
└── database/
    └── photos/              # 👥 Face database storage
```

## Usage Guide

### Setting Up Face Database

1. **Add Photos**: Place photos in the `database/photos/` directory
2. **Naming Convention**: Name files as `person_name.jpg` (e.g., `john_doe.jpg`, `jane_smith.png`)
3. **Photo Requirements**: 
   - Use clear, well-lit photos
   - Face should be clearly visible and frontal
   - Supported formats: JPG, PNG, JPEG
   - One photo per person recommended

Example structure:
```
database/photos/
├── john_doe.jpg
├── jane_smith.png
├── bob_wilson.jpeg
└── alice_johnson.jpg
```

### Real-Time Recognition

1. **Start the Application**:
   ```bash
   python app.py
   ```
   
2. **Open Browser**: Navigate to `http://localhost:5050`

3. **Start Recognition**: 
   - Click "Start Recognition" button
   - Allow camera access when prompted
   
4. **View Live Results**:
   - **Identity**: Person's name from filename or "Unknown"
   - **Gender**: Male/Female classification
   - **Emotion**: Current dominant emotion
   - **Confidence**: Recognition accuracy percentage
   - **Status**: Active/Inactive recognition state

5. **Stop Recognition**: 
   - Click "Stop Recognition" button

### Database Management

- **Add New Photos**: Place new photos in `database/photos/`
- **Reload Database**: Click "Reload Database" button to refresh without restart
- **Remove Photos**: Delete unwanted photos from the folder and reload

## Configuration

### Application Settings
```python
# In app.py, modify these settings:
app.run(debug=True, threaded=True, host='0.0.0.0', port=5050)
```

### Camera Settings
The system automatically:
- Uses camera index 0 (default webcam)
- Applies horizontal flip for mirror effect
- Detects faces using Haar Cascade classifier
- Runs recognition in separate threads for performance

### Recognition Models
DeepFace automatically downloads and uses:
- **Face Recognition**: Default DeepFace models
- **Gender Detection**: Built-in gender classification
- **Emotion Detection**: 7-emotion classification model

## 🛠️ Technical Details

### Face Recognition Process
1. **Face Detection**: OpenCV Haar Cascade detects faces in real-time
2. **Face Analysis**: DeepFace analyzes detected faces for gender and emotion
3. **Identity Matching**: Compares faces against database photos
4. **Results Display**: Shows results with confidence scores

### Performance Features
- **Threading**: Recognition runs in separate threads to avoid blocking
- **Caching**: Face cascade and models loaded once at startup
- **Error Handling**: Graceful handling of camera and recognition errors
- **Memory Management**: Efficient frame processing and cleanup

### API Endpoints
- `GET /` - Main interface
- `GET /video_feed` - Live camera stream
- `GET /start_recognition` - Start recognition process
- `GET /stop_recognition` - Stop recognition process
- `GET /get_results` - Get current recognition results
- `GET /reload_database` - Reload face database

## Troubleshooting

### Installation Issues

**TensorFlow Installation Problems:**
```bash
# Run the install script which handles TensorFlow properly:
python install.py

# For manual installation issues:
pip uninstall tensorflow tensorflow-macos tensorflow-metal -y
pip install tensorflow==2.13.0
```

**OpenCV Camera Issues:**
```bash
# Check camera permissions in browser
# Ensure no other applications are using the camera
# Try restarting the application
```

**DeepFace Model Download Issues:**
```bash
# Models download automatically on first use
# Ensure stable internet connection
# Check firewall settings
```

### Runtime Issues

**Camera Not Working:**
- Allow camera permissions in browser
- Check if camera is being used by other applications
- Restart the Flask application

**Recognition Not Working:**
- Ensure photos are in `database/photos/` folder
- Click "Reload Database" after adding photos
- Check photo quality and lighting
- Verify face is clearly visible in photos

**Slow Performance:**
- Close other resource-intensive applications
- Use good lighting for better face detection
- Ensure stable camera connection

**Browser Issues:**
- Use modern browsers (Chrome, Firefox, Safari, Edge)
- Enable camera permissions
- Check browser console for errors

## 🚀 Performance Optimization

### System Requirements
- **Minimum**: 4GB RAM, 2GB free disk space, webcam
- **Recommended**: 8GB RAM, 5GB free disk space, good lighting
- **Optimal**: 16GB RAM, SSD storage, high-quality webcam

### Optimization Tips
1. **Photo Quality**: Use clear, well-lit photos (224x224px minimum)
2. **Database Size**: Keep reasonable number of photos for best performance
3. **Lighting**: Ensure good lighting for both database photos and live recognition
4. **Camera Quality**: Use good quality webcam for better detection
5. **System Resources**: Close unnecessary applications during use

## 🔒 Security & Privacy

### Data Protection
- **Local Processing**: All recognition done locally, no cloud services
- **No External APIs**: All processing on your machine
- **Local Storage**: Face database stored locally
- **Privacy First**: No data transmission to external servers

### Security Features
- **Local Database**: Face photos stored only on your system
- **No Network Calls**: Recognition works offline after model download
- **Secure Processing**: All analysis done locally

## 📱 Browser Compatibility

### Supported Browsers
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 11+
- ✅ Edge 79+

### Camera Requirements
- WebRTC support required
- Camera permissions must be granted
- HTTPS recommended for production use

## 🔄 Maintenance

### Regular Tasks
```bash
# Backup face database
cp -r database/photos database/photos_backup

# Update dependencies
pip install --upgrade -r requirements.txt

# Clean restart
python app.py
```

### Database Management
```bash
# Add new photos to database/photos/
# Use descriptive filenames (person_name.jpg)
# Click "Reload Database" in web interface
# Remove poor quality photos for better accuracy
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/NewFeature`
3. Install dependencies: `python install.py`
4. Make your changes
5. Test thoroughly
6. Commit changes: `git commit -m 'Add NewFeature'`
7. Push to branch: `git push origin feature/NewFeature`
8. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add error handling for new features
- Test with different browsers and cameras

## 🙏 Acknowledgments

- **DeepFace** - Facial analysis framework by SefaIlkimen
- **OpenCV** - Computer vision library
- **TensorFlow** - Machine learning platform by Google
- **Flask** - Lightweight web framework
- **Haar Cascades** - Face detection classifiers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/IronxDevil/Facial-Recognition/issues)
- **Documentation**: This README and code comments
- **Community**: GitHub Discussions

## 🎯 Future Enhancements

### Planned Features
- [ ] **Multiple Face Recognition**: Recognize multiple faces simultaneously
- [ ] **Age Detection**: Add age estimation functionality
- [ ] **Photo Upload Interface**: Web-based photo management
- [ ] **Recognition History**: Track recognition events
- [ ] **Advanced Analytics**: Recognition statistics and reports
- [ ] **Mobile Optimization**: Better mobile device support

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

</div>