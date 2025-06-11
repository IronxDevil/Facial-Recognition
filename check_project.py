#!/usr/bin/env python3
"""
Project structure and dependency checker
"""
import os
import sys
import importlib

def check_project_structure():
    """Check if all required files and folders exist"""
    print("🔍 Checking project structure...\n")
    
    required_structure = {
        'files': [
            'app.py',
            'requirements.txt',
            'templates/index.html',
            'static/css/style.css',
            'static/js/script.js'
        ],
        'folders': [
            'templates',
            'static',
            'static/css',
            'static/js',
            'database',
            'database/photos'
        ]
    }
    
    missing_items = []
    
    # Check folders
    print("📁 Checking folders:")
    for folder in required_structure['folders']:
        if os.path.exists(folder):
            print(f"  ✅ {folder}")
        else:
            print(f"  ❌ {folder} - MISSING")
            missing_items.append(f"Folder: {folder}")
    
    # Check files
    print("\n📄 Checking files:")
    for file in required_structure['files']:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_items.append(f"File: {file}")
    
    # Check database photos
    photos_dir = 'database/photos'
    if os.path.exists(photos_dir):
        photos = [f for f in os.listdir(photos_dir) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"\n📸 Photos in database: {len(photos)}")
        if photos:
            for photo in photos[:5]:  # Show first 5
                name = os.path.splitext(photo)[0]
                print(f"  📷 {photo} → '{name}'")
            if len(photos) > 5:
                print(f"  ... and {len(photos) - 5} more")
        else:
            print("  ⚠️  No photos found - add some for face recognition")
    
    return missing_items

def check_dependencies():
    """Check if all required Python packages are installed"""
    print("\n🐍 Checking Python dependencies...\n")
    
    dependencies = [
        ('flask', 'Flask'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('tensorflow', 'TensorFlow'),
    ]
    
    missing_deps = []
    
    for module, name in dependencies:
        try:
            mod = importlib.import_module(module)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✅ {name}: {version}")
        except ImportError:
            print(f"  ❌ {name}: NOT INSTALLED")
            missing_deps.append(name)
    
    # Special check for DeepFace (can be slow to import)
    print("\n🤖 Checking DeepFace...")
    try:
        from deepface import DeepFace
        print("  ✅ DeepFace: Available")
    except ImportError:
        print("  ❌ DeepFace: NOT INSTALLED")
        missing_deps.append('DeepFace')
    except Exception as e:
        print(f"  ⚠️  DeepFace: Warning - {e}")
    
    return missing_deps

def check_camera_access():
    """Check if camera is accessible"""
    print("\n📹 Checking camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("  ✅ Camera access successful")
                print(f"  📐 Frame size: {frame.shape}")
            else:
                print("  ❌ Camera opened but cannot read frames")
            cap.release()
        else:
            print("  ❌ Cannot open camera")
    except Exception as e:
        print(f"  ❌ Camera check error: {e}")

def create_missing_structure():
    """Create missing folders and basic files"""
    print("\n🔧 Creating missing project structure...")
    
    # Create folders
    folders = ['templates', 'static/css', 'static/js', 'database/photos']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"  📁 Created: {folder}")
    
    # Create basic requirements.txt if missing
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            f.write("""Flask==2.3.3
opencv-python==4.8.1.78
deepface==0.0.75
numpy==1.24.3
Pillow==10.0.1
tensorflow==2.13.0
keras==2.13.1
protobuf==3.20.3
""")
        print("  📄 Created: requirements.txt")
    
    print("  ✅ Basic structure created!")

def main():
    print("🚀 Facial Recognition Project Checker\n")
    print("=" * 50)
    
    # Check project structure
    missing_structure = check_project_structure()
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    # Check camera
    check_camera_access()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if missing_structure:
        print("\n❌ Missing project files/folders:")
        for item in missing_structure:
            print(f"  • {item}")
        
        create_missing = input("\n🔧 Create missing structure? (y/n): ").lower().strip()
        if create_missing == 'y':
            create_missing_structure()
    
    if missing_deps:
        print("\n❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"  • {dep}")
        print(f"\n💡 Install with: pip install -r requirements.txt")
    
    if not missing_structure and not missing_deps:
        print("\n🎉 PROJECT READY TO RUN!")
        print("\n🚀 Start with: python app.py")
        print("🌐 Then open: http://localhost:5000")
    else:
        print(f"\n⚠️  Fix {len(missing_structure + missing_deps)} issues before running")

if __name__ == "__main__":
    main()