#!/usr/bin/env python3
"""
Dependency checker for Facial Recognition System
Run this before starting the main application
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
        return True

def install_package(package_name, pip_name=None):
    """Install a package using pip"""
    if pip_name is None:
        pip_name = package_name
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    dependencies = [
        ("flask", "Flask"),
        ("cv2", "opencv-python"),
        ("numpy", "numpy"),
        ("PIL", "Pillow"),
        ("tensorflow", "tensorflow-macos" if sys.platform == "darwin" else "tensorflow"),
    ]
    
    # Special handling for DeepFace
    deepface_deps = [
        ("deepface", "deepface"),
    ]
    
    print("🔍 Checking dependencies...\n")
    
    missing_deps = []
    
    for module_name, pip_name in dependencies:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} - OK")
        except ImportError:
            print(f"❌ {module_name} - Missing")
            missing_deps.append((module_name, pip_name))
    
    # Install missing dependencies
    if missing_deps:
        print(f"\n📦 Installing {len(missing_deps)} missing packages...")
        for module_name, pip_name in missing_deps:
            print(f"Installing {pip_name}...")
            if install_package(module_name, pip_name):
                print(f"✅ {pip_name} installed successfully")
            else:
                print(f"❌ Failed to install {pip_name}")
    
    # Check DeepFace separately (it's heavy)
    print("\n🤖 Checking DeepFace...")
    try:
        import deepface
        print("✅ DeepFace - OK")
    except ImportError:
        print("❌ DeepFace - Missing")
        print("📦 Installing DeepFace (this may take a while)...")
        if install_package("deepface", "deepface"):
            print("✅ DeepFace installed successfully")
        else:
            print("❌ Failed to install DeepFace")
    
    # Special Mac handling
    if sys.platform == "darwin":
        print("\n🍎 Mac detected - checking Metal acceleration...")
        try:
            import tensorflow as tf
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                print("✅ TensorFlow Metal acceleration available")
            else:
                print("⚠️  TensorFlow Metal not detected")
                print("💡 Install with: pip install tensorflow-metal")
        except:
            pass

def main():
    print("🔧 Facial Recognition System - Dependency Checker\n")
    
    if not check_python_version():
        sys.exit(1)
    
    check_and_install_dependencies()
    
    print("\n✅ Dependency check complete!")
    print("🚀 You can now run: python app.py")

if __name__ == "__main__":
    main()