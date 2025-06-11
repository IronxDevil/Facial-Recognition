#!/usr/bin/env python3
"""
Complete setup and compatibility checker for Facial Recognition System
This script will:
1. Check system compatibility
2. Resolve package conflicts
3. Install compatible versions
4. Test the installation
5. Verify everything works together
"""
import subprocess
import sys
import os
import platform
from datetime import datetime

class CompleteSetup:
    def __init__(self):
        self.system_info = {
            'platform': platform.system(),
            'architecture': platform.machine(),
            'is_apple_silicon': platform.machine() == 'arm64' and platform.system() == 'Darwin',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
        self.log_file = f"setup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    def log(self, message, also_print=True):
        """Log message to file and optionally print"""
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        if also_print:
            print(message)
    
    def run_command(self, command, description=""):
        """Run command with logging"""
        if description:
            self.log(f"🔄 {description}")
        
        try:
            result = subprocess.run(command, shell=True, check=True, 
                                  capture_output=True, text=True)
            self.log(f"✅ Command succeeded: {command}", False)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Command failed: {command}")
            self.log(f"Error: {e.stderr}", False)
            return False, e.stderr
    
    def step1_system_check(self):
        """Step 1: Check system compatibility"""
        self.log("\n" + "="*60)
        self.log("STEP 1: SYSTEM COMPATIBILITY CHECK")
        self.log("="*60)
        
        self.log(f"🖥️  System: {self.system_info['platform']} {self.system_info['architecture']}")
        self.log(f"🐍 Python: {self.system_info['python_version']}")
        
        # Check Python version
        if sys.version_info < (3, 8):
            self.log("❌ Python 3.8+ required!")
            return False
        
        if sys.version_info >= (3, 12):
            self.log("⚠️  Python 3.12+ detected - some packages may have compatibility issues")
        
        # Check pip
        success, _ = self.run_command(f"{sys.executable} -m pip --version", "Checking pip")
        if not success:
            self.log("❌ pip not available!")
            return False
        
        # Upgrade pip
        success, _ = self.run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
        
        self.log("✅ System compatibility check passed")
        return True
    
    def step2_conflict_resolution(self):
        """Step 2: Resolve package conflicts"""
        self.log("\n" + "="*60)
        self.log("STEP 2: PACKAGE CONFLICT RESOLUTION")
        self.log("="*60)
        
        # Get currently installed packages
        success, output = self.run_command(f"{sys.executable} -m pip list", "Getting installed packages")
        if not success:
            self.log("⚠️  Could not get package list")
        
        # Uninstall potentially conflicting packages
        conflicting_packages = [
            'tensorflow', 'tensorflow-macos', 'tensorflow-metal',
            'keras', 'tf-keras',
            'deepface',
            'opencv-python', 'opencv-contrib-python', 'opencv-python-headless',
            'numpy', 'pillow'
        ]
        
        self.log("🧹 Cleaning up existing installations...")
        for package in conflicting_packages:
            self.run_command(f"{sys.executable} -m pip uninstall {package} -y", 
                           f"Removing {package}")
        
        self.log("✅ Package cleanup completed")
        return True
    
    def step3_install_compatible_versions(self):
        """Step 3: Install compatible package versions"""
        self.log("\n" + "="*60)
        self.log("STEP 3: INSTALLING COMPATIBLE VERSIONS")
        self.log("="*60)
        
        # Define installation order and versions
        if self.system_info['is_apple_silicon']:
            self.log("🍎 Installing Apple Silicon optimized packages...")
            install_commands = [
                ("numpy==1.24.3", "NumPy"),
                ("Pillow==10.0.1", "Pillow"),
                ("opencv-python==4.8.1.78", "OpenCV"),
                ("Flask==2.3.3", "Flask"),
                ("protobuf==3.20.3", "Protobuf"),
                ("tensorflow-macos==2.13.0", "TensorFlow macOS"),
                ("tensorflow-metal==1.0.1", "TensorFlow Metal"),
                ("keras==2.13.1", "Keras"),
                ("pandas>=1.3.0", "Pandas"),
                ("gdown>=4.6.0", "GDown"),
                ("tqdm>=4.64.0", "TQDM"),
                ("deepface==0.0.75", "DeepFace")
            ]
        else:
            self.log("💻 Installing standard packages...")
            install_commands = [
                ("numpy==1.24.3", "NumPy"),
                ("Pillow==10.0.1", "Pillow"),
                ("opencv-python==4.8.1.78", "OpenCV"),
                ("Flask==2.3.3", "Flask"),
                ("protobuf==3.20.3", "Protobuf"),
                ("tensorflow==2.13.0", "TensorFlow"),
                ("keras==2.13.1", "Keras"),
                ("pandas>=1.3.0", "Pandas"),
                ("gdown>=4.6.0", "GDown"),
                ("tqdm>=4.64.0", "TQDM"),
                ("deepface==0.0.75", "DeepFace")
            ]
        
        # Install packages in order
        failed_packages = []
        for package, name in install_commands:
            success, output = self.run_command(
                f"{sys.executable} -m pip install {package}", 
                f"Installing {name}"
            )
            if not success:
                failed_packages.append((package, name))
                self.log(f"❌ Failed to install {name}")
            else:
                self.log(f"✅ {name} installed successfully")
        
        if failed_packages:
            self.log(f"\n⚠️  {len(failed_packages)} packages failed to install:")
            for package, name in failed_packages:
                self.log(f"  - {name} ({package})")
            return False
        
        self.log("✅ All packages installed successfully")
        return True
    
    def step4_compatibility_test(self):
        """Step 4: Test package compatibility"""
        self.log("\n" + "="*60)
        self.log("STEP 4: COMPATIBILITY TESTING")
        self.log("="*60)
        
        tests = [
            ("NumPy", "import numpy as np; print(f'NumPy {np.__version__}')"),
            ("OpenCV", "import cv2; print(f'OpenCV {cv2.__version__}')"),
            ("Flask", "from flask import Flask; import flask; print(f'Flask {flask.__version__}')"),
            ("TensorFlow", "import tensorflow as tf; print(f'TensorFlow {tf.__version__}')"),
            ("Keras", "from tensorflow import keras; print(f'Keras {keras.__version__}')"),
            ("Pillow", "from PIL import Image; import PIL; print(f'Pillow {PIL.__version__}')"),
        ]
        
        failed_tests = []
        
        for test_name, test_code in tests:
            try:
                exec(test_code)
                self.log(f"✅ {test_name} - OK")
            except Exception as e:
                self.log(f"❌ {test_name} - Error: {e}")
                failed_tests.append((test_name, str(e)))
        
        # Test DeepFace separately (it's slow)
        self.log("\n🤖 Testing DeepFace (this may take a moment)...")
        try:
            from deepface import DeepFace
            import numpy as np
            
            # Test basic functionality
            test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            result = DeepFace.analyze(test_img, actions=['emotion'], 
                                    enforce_detection=False, silent=True)
            self.log("✅ DeepFace - OK")
            
        except Exception as e:
            self.log(f"❌ DeepFace - Error: {e}")
            failed_tests.append(("DeepFace", str(e)))
        
        if failed_tests:
            self.log(f"\n❌ {len(failed_tests)} compatibility tests failed:")
            for test_name, error in failed_tests:
                self.log(f"  - {test_name}: {error}")
            return False
        
        self.log("✅ All compatibility tests passed")
        return True
    
    def step5_final_verification(self):
        """Step 5: Final system verification"""
        self.log("\n" + "="*60)
        self.log("STEP 5: FINAL VERIFICATION")
        self.log("="*60)
        
        # Check if all required files exist
        required_files = ['app.py']
        required_dirs = ['templates', 'static', 'database/photos']
        
        missing_items = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_items.append(f"File: {file}")
        
        for dir in required_dirs:
            if not os.path.exists(dir):
                missing_items.append(f"Directory: {dir}")
                # Create missing directories
                os.makedirs(dir, exist_ok=True)
                self.log(f"📁 Created directory: {dir}")
        
        if missing_items:
            self.log("⚠️  Missing project files:")
            for item in missing_items:
                self.log(f"  - {item}")
        
        # Test camera access
        self.log("\n📹 Testing camera access...")
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    self.log("✅ Camera access successful")
                else:
                    self.log("⚠️  Camera opened but cannot read frames")
                cap.release()
            else:
                self.log("⚠️  Cannot open camera (may need permissions)")
        except Exception as e:
            self.log(f"⚠️  Camera test error: {e}")
        
        self.log("✅ Final verification completed")
        return True
    
    def create_project_files(self):
        """Create missing project files"""
        self.log("\n📄 Creating missing project files...")
        
        # Create requirements.txt
        requirements_content = """# Facial Recognition System - Standard
numpy==1.24.3
Pillow==10.0.1
opencv-python==4.8.1.78
Flask==2.3.3
tensorflow==2.13.0
keras==2.13.1
deepface==0.0.75
protobuf==3.20.3
pandas>=1.3.0
gdown>=4.6.0
tqdm>=4.64.0
"""
        
        with open('requirements_final.txt', 'w') as f:
            f.write(requirements_content)
        self.log("📄 Created requirements_final.txt")
        
        # Create run script
        run_script = """#!/usr/bin/env python3
'''
Facial Recognition System Launcher
'''
import sys
import os

def check_dependencies():
    required_packages = ['flask', 'cv2', 'tensorflow', 'deepface', 'numpy']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("🔧 Run: python setup_complete.py")
        return False
    
    return True

def main():
    print("🎭 Facial Recognition System")
    print("=" * 40)
    
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies available")
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found!")
        print("Please ensure the main application file exists")
        sys.exit(1)
    
    # Check database directory
    os.makedirs('database/photos', exist_ok=True)
    
    print("🚀 Starting application...")
    print("📱 Open: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    
    # Import and run the app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print("❌ Could not import app.py")
        print("Please check your main application file")
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

if __name__ == "__main__":
    main()
"""
        
        with open('run_app.py', 'w') as f:
            f.write(run_script)
        self.log("📄 Created run_app.py")
    
    def run_complete_setup(self):
        """Run the complete setup process"""
        self.log("🎭 FACIAL RECOGNITION SYSTEM - COMPLETE SETUP")
        self.log("=" * 60)
        self.log(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"📋 Log file: {self.log_file}")
        
        steps = [
            ("System Compatibility Check", self.step1_system_check),
            ("Package Conflict Resolution", self.step2_conflict_resolution),
            ("Install Compatible Versions", self.step3_install_compatible_versions),
            ("Compatibility Testing", self.step4_compatibility_test),
            ("Final Verification", self.step5_final_verification)
        ]
        
        completed_steps = 0
        
        for step_name, step_function in steps:
            self.log(f"\n🔄 Starting: {step_name}")
            
            try:
                if step_function():
                    completed_steps += 1
                    self.log(f"✅ Completed: {step_name}")
                else:
                    self.log(f"❌ Failed: {step_name}")
                    break
            except Exception as e:
                self.log(f"❌ Error in {step_name}: {e}")
                break
        
        # Create project files
        self.create_project_files()
        
        # Final report
        self.log("\n" + "="*60)
        self.log("📊 SETUP COMPLETE")
        self.log("="*60)
        
        self.log(f"✅ Completed steps: {completed_steps}/{len(steps)}")
        
        if completed_steps == len(steps):
            self.log("🎉 SETUP SUCCESSFUL!")
            self.log("\n🚀 Next steps:")
            self.log("1. python run_app.py")
            self.log("2. Open http://localhost:5000")
            self.log("3. Add photos to database/photos/")
            self.log("4. Click 'Reload Database' in web interface")
            
            # Show system info
            self.log(f"\n📋 System Configuration:")
            self.log(f"  🖥️  Platform: {self.system_info['platform']} {self.system_info['architecture']}")
            self.log(f"  🐍 Python: {self.system_info['python_version']}")
            if self.system_info['is_apple_silicon']:
                self.log(f"  🍎 Apple Silicon optimization: Enabled")
            
            return True
        else:
            self.log("❌ SETUP FAILED!")
            self.log(f"📋 Check log file: {self.log_file}")
            self.log("🔧 Try manual installation or contact support")
            return False

def main():
    setup = CompleteSetup()
    return setup.run_complete_setup()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)