#!/usr/bin/env python3
"""
Quick compatibility test for facial recognition system
"""
import sys
import traceback
import subprocess

def test_critical_compatibility():
    """Test critical package compatibility"""
    print("🧪 Testing Critical Package Compatibility\n")
    
    tests = []
    
    # Test 1: TensorFlow and Keras compatibility
    print("1️⃣ Testing TensorFlow + Keras...")
    try:
        import tensorflow as tf
        from tensorflow import keras
        
        # Test basic operations
        x = tf.constant([1, 2, 3, 4])
        y = tf.constant([2, 3, 4, 5])
        result = tf.add(x, y)
        
        # Test keras
        model = keras.Sequential([keras.layers.Dense(1, input_shape=(1,))])
        
        print(f"   ✅ TensorFlow {tf.__version__} + Keras {keras.__version__}")
        tests.append(True)
        
    except Exception as e:
        print(f"   ❌ TensorFlow/Keras error: {e}")
        tests.append(False)
    
    # Test 2: DeepFace with TensorFlow
    print("\n2️⃣ Testing DeepFace + TensorFlow...")
    try:
        from deepface import DeepFace
        import numpy as np
        
        # Create test image
        test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Test emotion analysis
        result = DeepFace.analyze(
            test_img, 
            actions=['emotion'], 
            enforce_detection=False,
            silent=True
        )
        
        print(f"   ✅ DeepFace analysis successful")
        tests.append(True)
        
    except Exception as e:
        print(f"   ❌ DeepFace error: {e}")
        tests.append(False)
    
    # Test 3: OpenCV compatibility
    print("\n3️⃣ Testing OpenCV...")
    try:
        import cv2
        import numpy as np
        
        # Test basic operations
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Test face cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if face_cascade.empty():
            raise Exception("Face cascade not loaded")
        
        print(f"   ✅ OpenCV {cv2.__version__}")
        tests.append(True)
        
    except Exception as e:
        print(f"   ❌ OpenCV error: {e}")
        tests.append(False)
    
    # Test 4: Flask compatibility
    print("\n4️⃣ Testing Flask...")
    try:
        from flask import Flask, Response, jsonify
        
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return jsonify({'status': 'ok'})
        
        print(f"   ✅ Flask app creation successful")
        tests.append(True)
        
    except Exception as e:
        print(f"   ❌ Flask error: {e}")
        tests.append(False)
    
    # Test 5: Memory compatibility test
    print("\n5️⃣ Testing memory usage...")
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        print(f"   📊 Current memory usage: {memory_mb:.1f} MB")
        
        if memory_mb > 1000:  # More than 1GB
            print(f"   ⚠️  High memory usage detected")
        else:
            print(f"   ✅ Memory usage normal")
        
        tests.append(True)
        
    except ImportError:
        print(f"   ℹ️  psutil not available (optional)")
        tests.append(True)
    except Exception as e:
        print(f"   ❌ Memory test error: {e}")
        tests.append(False)
    
    # Summary
    passed = sum(tests)
    total = len(tests)
    
    print(f"\n" + "="*50)
    print(f"📊 COMPATIBILITY TEST RESULTS")
    print(f"="*50)
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print(f"🎉 ALL COMPATIBILITY TESTS PASSED!")
        print(f"🚀 Your system is ready to run: python app.py")
        return True
    else:
        print(f"❌ {total - passed} compatibility issues found")
        print(f"🔧 Run: python compatibility_checker.py for detailed analysis")
        return False

def resolve_conflicts():
    """Resolve package conflicts"""
    print("🔧 Resolving package conflicts...\n")
    
    conflicts = [
        {'group': 'tensorflow', 'installed': ['tensorflow', 'tensorflow-gpu']},
        {'group': 'opencv', 'installed': ['opencv-python', 'opencv-contrib-python']}
    ]
    
    for conflict in conflicts:
        if 'tensorflow' in conflict['group']:
            # Prefer tensorflow over tensorflow-gpu for our use case
            keep = 'tensorflow'
            remove = [p for p in conflict['installed'] if p != keep]
            
            print(f"   🔄 Recommended: Keep {keep}, remove {', '.join(remove)}")
            
            choice = input(f"   Resolve automatically? (y/n): ").lower().strip()
            if choice == 'y':
                for pkg in remove:
                    print(f"   🗑️  Uninstalling {pkg}...")
                    try:
                        subprocess.run([sys.executable, '-m', 'pip', 'uninstall', pkg, '-y'], 
                                     check=True, capture_output=True)
                        print(f"   ✅ Removed {pkg}")
                    except subprocess.CalledProcessError as e:
                        print(f"   ❌ Failed to remove {pkg}: {e}")
                        return False
        
        elif 'opencv' in conflict['group']:
            # Prefer opencv-python over opencv-contrib-python for our use case
            keep = 'opencv-python'
            remove = [p for p in conflict['installed'] if p != keep]
            
            print(f"   🔄 Recommended: Keep {keep}, remove {', '.join(remove)}")
            
            choice = input(f"   Resolve automatically? (y/n): ").lower().strip()
            if choice == 'y':
                for pkg in remove:
                    print(f"   🗑️  Uninstalling {pkg}...")
                    try:
                        subprocess.run([sys.executable, '-m', 'pip', 'uninstall', pkg, '-y'], 
                                     check=True, capture_output=True)
                        print(f"   ✅ Removed {pkg}")
                    except subprocess.CalledProcessError as e:
                        print(f"   ❌ Failed to remove {pkg}: {e}")
                        return False
    
    print(f"\n🎉 All conflicts resolved!")
    return True

def main():
    print("🔧 Package Conflict Resolver\n")
    
    if resolve_conflicts():
        print("\n✅ System is ready for installation!")
        print("🚀 Next step: python install_compatible.py")
    else:
        print("\n❌ Some conflicts could not be resolved automatically")
        print("🔧 Manual intervention required")

if __name__ == "__main__":
    success = test_critical_compatibility()
    sys.exit(0 if success else 1)