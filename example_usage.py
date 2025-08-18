#!/usr/bin/env python3
"""
Example usage script for Azure Custom Vision RTSP Detector

This script demonstrates different ways to use the detector with various configurations.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_files():
    """Check if required files exist."""
    required_files = [
        'azure_cv_rtsp_detector.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Error: Missing required files: {missing_files}")
        return False
    
    return True

def example_basic_usage():
    """Show basic usage example."""
    print("Basic Usage Example:")
    print("-" * 30)
    
    model_path = input("Enter path to your ONNX model file: ").strip()
    rtsp_url = input("Enter your RTSP stream URL: ").strip()
    
    if not model_path or not rtsp_url:
        print("Both model path and RTSP URL are required.")
        return
    
    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"Error: Model file not found: {model_path}")
        return
    
    command = [
        sys.executable,
        'azure_cv_rtsp_detector.py',
        '--model', model_path,
        '--rtsp', rtsp_url
    ]
    
    print(f"\nRunning command: {' '.join(command)}")
    print("Press Ctrl+C to stop the detector")
    print("Press 'q' in the video window to quit")
    
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print("\nDetector stopped by user")

def example_headless_mode():
    """Show headless mode example."""
    print("Headless Mode Example:")
    print("-" * 30)
    
    model_path = input("Enter path to your ONNX model file: ").strip()
    rtsp_url = input("Enter your RTSP stream URL: ").strip()
    
    if not model_path or not rtsp_url:
        print("Both model path and RTSP URL are required.")
        return
    
    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"Error: Model file not found: {model_path}")
        return
    
    command = [
        sys.executable,
        'azure_cv_rtsp_detector.py',
        '--model', model_path,
        '--rtsp', rtsp_url,
        '--no-display',
        '--save-results',
        '--log-level', 'INFO'
    ]
    
    print(f"\nRunning command: {' '.join(command)}")
    print("Running in headless mode - no video window will appear")
    print("Results will be saved to a JSON file")
    print("Press Ctrl+C to stop the detector")
    
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print("\nDetector stopped by user")

def test_rtsp_connection():
    """Test RTSP connection without running full detection."""
    print("RTSP Connection Test:")
    print("-" * 30)
    
    rtsp_url = input("Enter your RTSP stream URL to test: ").strip()
    
    if not rtsp_url:
        print("RTSP URL is required.")
        return
    
    print("Testing RTSP connection...")
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(rtsp_url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        if not cap.isOpened():
            print("✗ Failed to connect to RTSP stream")
            print("Please check:")
            print("  - RTSP URL format")
            print("  - Network connectivity")
            print("  - Authentication credentials")
            return
        
        print("✓ Successfully connected to RTSP stream")
        
        # Try to read a frame
        ret, frame = cap.read()
        if ret:
            height, width, channels = frame.shape
            print(f"✓ Successfully read frame: {width}x{height}, {channels} channels")
        else:
            print("✗ Failed to read frame from stream")
        
        cap.release()
        
    except ImportError:
        print("✗ OpenCV not installed. Please install requirements first.")
    except Exception as e:
        print(f"✗ Error testing RTSP connection: {e}")

def show_sample_commands():
    """Show sample command examples."""
    print("Sample Commands:")
    print("-" * 30)
    
    commands = [
        {
            "description": "Basic detection with display",
            "command": "python azure_cv_rtsp_detector.py --model model.onnx --rtsp rtsp://192.168.1.100:554/stream"
        },
        {
            "description": "Headless mode with results saving",
            "command": "python azure_cv_rtsp_detector.py --model model.onnx --rtsp rtsp://user:pass@192.168.1.100/stream --no-display --save-results"
        },
        {
            "description": "Debug mode with verbose logging",
            "command": "python azure_cv_rtsp_detector.py --model model.onnx --rtsp rtsp://192.168.1.100/stream --log-level DEBUG"
        },
        {
            "description": "IP camera with authentication",
            "command": "python azure_cv_rtsp_detector.py --model model.onnx --rtsp rtsp://admin:password@192.168.1.100/Streaming/Channels/101"
        }
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n{i}. {cmd['description']}:")
        print(f"   {cmd['command']}")

def main():
    """Main menu."""
    if not check_files():
        return
    
    while True:
        print("\nAzure Custom Vision RTSP Detector - Example Usage")
        print("=" * 50)
        print("1. Basic Usage (with video display)")
        print("2. Headless Mode (no display, save results)")
        print("3. Test RTSP Connection")
        print("4. Show Sample Commands")
        print("5. Install Dependencies")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            example_basic_usage()
        elif choice == '2':
            example_headless_mode()
        elif choice == '3':
            test_rtsp_connection()
        elif choice == '4':
            show_sample_commands()
        elif choice == '5':
            print("Installing dependencies...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                print("Dependencies installed successfully!")
            except Exception as e:
                print(f"Error installing dependencies: {e}")
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()