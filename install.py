#!/usr/bin/env python3
"""
Simple installation script for Facial Recognition System
Uses standard TensorFlow for maximum compatibility
"""
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🎭 Facial Recognition System - Simple Installation")
    print("=" * 50)
    
    # Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Clean install - remove any existing tensorflow variants
    print("\n🧹 Cleaning existing installations...")
    cleanup_packages = [
        "tensorflow-macos", 
        "tensorflow-metal", 
        "tensorflow", 
        "deepface", 
        "opencv-python"
    ]
    
    for package in cleanup_packages:
        subprocess.run(f"{sys.executable} -m pip uninstall {package} -y", 
                      shell=True, capture_output=True)
    
    # Install from requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing packages"):
        return False
    
    # Test installation
    print("\n🧪 Testing installation...")
    try:
        import tensorflow as tf
        import cv2
        from deepface import DeepFace
        import numpy as np
        from flask import Flask
        
        print(f"✅ TensorFlow: {tf.__version__}")
        print(f"✅ OpenCV: {cv2.__version__}")
        print(f"✅ NumPy: {np.__version__}")
        print("✅ DeepFace: Imported successfully")
        print("✅ Flask: Imported successfully")
        
        # Quick functionality test
        test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        result = DeepFace.analyze(test_img, actions=['emotion'], 
                                enforce_detection=False, silent=True)
        print("✅ DeepFace functionality test passed")
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False
    
    print("\n🎉 Installation completed successfully!")
    print("🚀 Run: python app.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)