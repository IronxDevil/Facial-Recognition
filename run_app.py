#!/usr/bin/env python3
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
        print("
👋 Application stopped")

if __name__ == "__main__":
    main()
