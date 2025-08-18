#!/usr/bin/env python3
"""
Test script to verify the setup and dependencies for Azure Custom Vision RTSP Detector
"""

import sys
import importlib
import subprocess
import os

def test_python_version():
    """Test Python version compatibility."""
    print("Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not supported. Requires Python 3.8+")
        return False

def test_dependencies():
    """Test required dependencies."""
    print("\nTesting dependencies...")
    
    required_packages = {
        'cv2': 'opencv-python',
        'onnxruntime': 'onnxruntime',
        'numpy': 'numpy',
        'PIL': 'Pillow'
    }
    
    all_good = True
    
    for module_name, package_name in required_packages.items():
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, '__version__'):
                version = module.__version__
            else:
                version = "unknown"
            print(f"✓ {package_name} ({version}) is installed")
        except ImportError:
            print(f"✗ {package_name} is not installed")
            all_good = False
    
    return all_good

def test_opencv_functionality():
    """Test OpenCV video capture functionality."""
    print("\nTesting OpenCV video capture...")
    
    try:
        import cv2
        
        # Test basic OpenCV functionality
        test_image = cv2.imread('test_image.jpg')  # This will fail gracefully
        
        # Test video capture creation (doesn't actually connect)
        cap = cv2.VideoCapture()
        if cap is not None:
            print("✓ OpenCV VideoCapture can be created")
            cap.release()
        else:
            print("✗ OpenCV VideoCapture creation failed")
            return False
            
        print("✓ OpenCV basic functionality works")
        return True
        
    except Exception as e:
        print(f"✗ OpenCV test failed: {e}")
        return False

def test_onnx_runtime():
    """Test ONNX Runtime functionality."""
    print("\nTesting ONNX Runtime...")
    
    try:
        import onnxruntime as ort
        
        # Get available providers
        providers = ort.get_available_providers()
        print(f"✓ ONNX Runtime available providers: {providers}")
        
        # Check for GPU support
        if 'CUDAExecutionProvider' in providers:
            print("✓ GPU acceleration (CUDA) is available")
        elif 'DmlExecutionProvider' in providers:
            print("✓ GPU acceleration (DirectML) is available")
        else:
            print("ℹ Only CPU execution is available")
        
        return True
        
    except Exception as e:
        print(f"✗ ONNX Runtime test failed: {e}")
        return False

def test_file_permissions():
    """Test file system permissions."""
    print("\nTesting file permissions...")
    
    try:
        # Test write permissions
        test_file = 'test_write_permissions.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✓ Write permissions are available")
        
        return True
        
    except Exception as e:
        print(f"✗ File permission test failed: {e}")
        return False

def install_missing_dependencies():
    """Attempt to install missing dependencies."""
    print("\nAttempting to install missing dependencies...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Dependencies installed successfully")
            return True
        else:
            print(f"✗ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Installation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Azure Custom Vision RTSP Detector - Setup Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_opencv_functionality,
        test_onnx_runtime,
        test_file_permissions
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    
    if all(results):
        print("✓ All tests passed! Your setup is ready.")
        print("\nYou can now run the detector with:")
        print("python azure_cv_rtsp_detector.py --model your_model.onnx --rtsp your_rtsp_url")
    else:
        print("✗ Some tests failed. Please address the issues above.")
        
        if not results[1]:  # Dependencies test failed
            print("\nTry installing dependencies with:")
            print("pip install -r requirements.txt")
            
            response = input("\nWould you like to try installing dependencies now? (y/n): ")
            if response.lower() == 'y':
                install_missing_dependencies()

if __name__ == "__main__":
    main()