#!/bin/bash

# Azure Custom Vision RTSP Detector - Launch Script
# This script provides an easy way to run the detector with common configurations

echo "Azure Custom Vision RTSP Detector"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required files exist
if [ ! -f "azure_cv_rtsp_detector.py" ]; then
    echo "Error: azure_cv_rtsp_detector.py not found"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Function to install dependencies
install_deps() {
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "Dependencies installed successfully!"
    else
        echo "Error installing dependencies"
        exit 1
    fi
}

# Function to run basic detection
run_basic() {
    echo "Basic Detection Mode"
    echo "-------------------"
    
    read -p "Enter path to ONNX model file: " MODEL_PATH
    read -p "Enter RTSP stream URL: " RTSP_URL
    
    if [ -z "$MODEL_PATH" ] || [ -z "$RTSP_URL" ]; then
        echo "Error: Both model path and RTSP URL are required"
        return 1
    fi
    
    if [ ! -f "$MODEL_PATH" ]; then
        echo "Error: Model file not found: $MODEL_PATH"
        return 1
    fi
    
    echo "Starting detector..."
    echo "Press Ctrl+C to stop, or 'q' in video window to quit"
    
    python3 azure_cv_rtsp_detector.py --model "$MODEL_PATH" --rtsp "$RTSP_URL"
}

# Function to run headless mode
run_headless() {
    echo "Headless Mode (No Display)"
    echo "-------------------------"
    
    read -p "Enter path to ONNX model file: " MODEL_PATH
    read -p "Enter RTSP stream URL: " RTSP_URL
    
    if [ -z "$MODEL_PATH" ] || [ -z "$RTSP_URL" ]; then
        echo "Error: Both model path and RTSP URL are required"
        return 1
    fi
    
    if [ ! -f "$MODEL_PATH" ]; then
        echo "Error: Model file not found: $MODEL_PATH"
        return 1
    fi
    
    echo "Starting detector in headless mode..."
    echo "Results will be saved to JSON file"
    echo "Press Ctrl+C to stop"
    
    python3 azure_cv_rtsp_detector.py --model "$MODEL_PATH" --rtsp "$RTSP_URL" --no-display --save-results
}

# Function to test setup
test_setup() {
    echo "Testing setup..."
    if [ -f "test_setup.py" ]; then
        python3 test_setup.py
    else
        echo "test_setup.py not found, running basic test..."
        python3 -c "import cv2, onnxruntime, numpy; print('Basic dependencies are available')"
    fi
}

# Main menu
while true; do
    echo ""
    echo "Select an option:"
    echo "1. Install Dependencies"
    echo "2. Test Setup"
    echo "3. Run Basic Detection (with video display)"
    echo "4. Run Headless Mode (no display, save results)"
    echo "5. Show Help"
    echo "6. Exit"
    echo ""
    
    read -p "Enter your choice (1-6): " CHOICE
    
    case $CHOICE in
        1)
            install_deps
            ;;
        2)
            test_setup
            ;;
        3)
            run_basic
            ;;
        4)
            run_headless
            ;;
        5)
            echo ""
            echo "Usage Examples:"
            echo "python3 azure_cv_rtsp_detector.py --model model.onnx --rtsp rtsp://192.168.1.100:554/stream"
            echo "python3 azure_cv_rtsp_detector.py --model model.onnx --rtsp rtsp://user:pass@192.168.1.100/stream --no-display --save-results"
            echo ""
            echo "For more help, see README_DETECTOR.md"
            ;;
        6)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select 1-6."
            ;;
    esac
done