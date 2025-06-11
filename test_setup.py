import tensorflow as tf
import cv2
from deepface import DeepFace
import numpy as np

def test_tensorflow_setup():
    """Test TensorFlow Metal setup"""
    print("=== TensorFlow Setup Test ===")
    print(f"TensorFlow version: {tf.__version__}")
    print(f"GPU Available: {tf.config.list_physical_devices('GPU')}")
    print(f"Metal Plugin Available: {len(tf.config.list_physical_devices('GPU')) > 0}")
    
    # Test basic computation
    with tf.device('/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'):
        a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
        b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
        c = tf.matmul(a, b)
        print(f"Matrix multiplication test: {c.numpy()}")

def test_opencv():
    """Test OpenCV camera access"""
    print("\n=== OpenCV Camera Test ===")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("✅ Camera access successful")
        ret, frame = cap.read()
        if ret:
            print(f"✅ Frame capture successful - Shape: {frame.shape}")
        else:
            print("❌ Frame capture failed")
        cap.release()
    else:
        print("❌ Camera access failed")

def test_deepface():
    """Test DeepFace functionality"""
    print("\n=== DeepFace Test ===")
    try:
        # Create a test image
        test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Test emotion and gender detection
        result = DeepFace.analyze(
            test_img, 
            actions=['emotion', 'gender'], 
            enforce_detection=False,
            silent=True
        )
        print("✅ DeepFace analysis successful")
        print(f"   - Detected emotion: {result[0]['dominant_emotion']}")
        print(f"   - Detected gender: {result[0]['dominant_gender']}")
        
    except Exception as e:
        print(f"❌ DeepFace test failed: {e}")

def test_performance():
    """Test performance with Metal acceleration"""
    print("\n=== Performance Test ===")
    import time
    
    # Test TensorFlow performance
    start_time = time.time()
    with tf.device('/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'):
        # Simulate face recognition workload
        x = tf.random.normal((100, 224, 224, 3))
        y = tf.keras.applications.VGG16(weights=None, include_top=False)(x)
    
    end_time = time.time()
    device = "GPU (Metal)" if tf.config.list_physical_devices('GPU') else "CPU"
    print(f"Neural network inference on {device}: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    test_tensorflow_setup()
    test_opencv()
    test_deepface()
    test_performance()
    print("\n=== Setup Test Complete ===")