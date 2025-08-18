# Azure Custom Vision AI ONNX Model RTSP Stream Detector

A Python application that uses ONNX models exported from Azure Custom Vision AI to perform real-time object detection and classification on RTSP video streams.

## Features

- **ONNX Model Support**: Compatible with models exported from Azure Custom Vision AI
- **RTSP Stream Processing**: Real-time processing of RTSP video streams
- **Real-time Detection**: Live object detection and classification
- **Configurable Display**: Option to run with or without video display (headless mode)
- **Results Logging**: Save detection results to JSON files
- **Performance Monitoring**: FPS monitoring and logging
- **Flexible Input**: Support for various RTSP stream formats

## Requirements

- Python 3.8 or higher
- OpenCV for video processing
- ONNX Runtime for model inference
- RTSP-compatible camera or stream source
- ONNX model exported from Azure Custom Vision AI

## Installation

1. **Clone or download the application files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Alternative installation using setup.py:**
   ```bash
   pip install -e .
   ```

## Usage

### Basic Usage

```bash
python azure_cv_rtsp_detector.py --model path/to/your/model.onnx --rtsp rtsp://your-stream-url
```

### Command Line Arguments

- `--model, -m`: **Required**. Path to the ONNX model file exported from Azure Custom Vision AI
- `--rtsp, -r`: **Required**. RTSP stream URL
- `--no-display`: Optional. Run without displaying video window (headless mode)
- `--save-results`: Optional. Save detection results to JSON file
- `--log-level`: Optional. Set logging level (DEBUG, INFO, WARNING, ERROR). Default: INFO

### Examples

1. **Basic detection with video display:**
   ```bash
   python azure_cv_rtsp_detector.py --model my_model.onnx --rtsp rtsp://192.168.1.100:554/stream
   ```

2. **Headless mode with result saving:**
   ```bash
   python azure_cv_rtsp_detector.py --model my_model.onnx --rtsp rtsp://user:pass@192.168.1.100/stream --no-display --save-results
   ```

3. **With authentication and debug logging:**
   ```bash
   python azure_cv_rtsp_detector.py --model my_model.onnx --rtsp rtsp://username:password@192.168.1.100:554/stream --log-level DEBUG
   ```

## RTSP URL Formats

The application supports various RTSP URL formats:

- Basic: `rtsp://192.168.1.100:554/stream`
- With authentication: `rtsp://username:password@192.168.1.100:554/stream`
- Different ports: `rtsp://192.168.1.100:8554/live/stream`
- IP cameras: `rtsp://admin:password@192.168.1.100/Streaming/Channels/101`

## Azure Custom Vision AI Model Export

To use this application, you need to export your trained model from Azure Custom Vision AI:

1. **Train your model** in Azure Custom Vision portal
2. **Go to Performance tab** in your project
3. **Click Export** button
4. **Select ONNX format**
5. **Download the exported model**
6. **Use the downloaded .onnx file** with this application

### Supported Model Types

- **Classification models**: Single-label and multi-label classification
- **Object Detection models**: Bounding box detection (requires model output adaptation)

## Configuration

### Model Input Requirements

The application automatically handles:
- **Image resizing** to match model input dimensions
- **Color space conversion** (BGR to RGB)
- **Normalization** to [0, 1] range
- **Format conversion** to NCHW format if needed

### Performance Tuning

- **Frame Processing**: By default, processes every 5th frame for better performance
- **Buffer Size**: RTSP buffer size is set to 1 to reduce latency
- **Confidence Threshold**: Minimum confidence threshold is set to 0.1 (10%)

You can modify these settings in the code:
```python
# In RTSPStreamProcessor.process_stream()
if frame_count % 5 == 0:  # Change this value to process more/fewer frames

# In AzureCustomVisionDetector._process_outputs()
if confidence > 0.1:  # Change this threshold
```

## Output

### Console Output
- Real-time FPS information
- Detection results with confidence scores
- Connection status and errors

### Video Display
- Live video stream with overlay text
- Top 5 predictions displayed on screen
- Timestamp overlay

### JSON Results (when --save-results is used)
```json
[
  {
    "timestamp": 1640995200.123,
    "frame": 150,
    "predictions": [
      {
        "label": "Class_0",
        "confidence": 0.85,
        "class_id": 0
      }
    ]
  }
]
```

## Troubleshooting

### Common Issues

1. **"Failed to connect to RTSP stream"**
   - Check RTSP URL format
   - Verify network connectivity
   - Ensure camera/stream is accessible
   - Check authentication credentials

2. **"Error loading model"**
   - Verify ONNX model file path
   - Ensure model is compatible with ONNX Runtime version
   - Check model was exported correctly from Azure Custom Vision

3. **Poor performance/Low FPS**
   - Reduce frame processing frequency
   - Use GPU acceleration (install `onnxruntime-gpu`)
   - Lower video resolution if possible

4. **"Failed to read frame"**
   - Network connectivity issues
   - Stream may be temporarily unavailable
   - RTSP stream format not supported

### GPU Acceleration

For better performance with NVIDIA GPUs:

1. **Install CUDA-compatible ONNX Runtime:**
   ```bash
   pip uninstall onnxruntime
   pip install onnxruntime-gpu
   ```

2. **Verify CUDA installation:**
   ```bash
   python -c "import onnxruntime as ort; print(ort.get_available_providers())"
   ```

## Architecture

### Classes

1. **AzureCustomVisionDetector**: Handles ONNX model loading and inference
2. **RTSPStreamProcessor**: Manages RTSP stream connection and video processing

### Key Methods

- `preprocess_image()`: Prepares images for model input
- `predict()`: Runs inference on input images
- `process_stream()`: Main loop for stream processing
- `_draw_predictions()`: Overlays results on video frames

## License

This project is provided as-is for educational and development purposes.

## Support

For issues related to:
- **Azure Custom Vision**: Check Azure documentation
- **ONNX Runtime**: Visit ONNX Runtime GitHub repository
- **OpenCV**: Refer to OpenCV documentation
- **RTSP Streams**: Consult your camera/device documentation