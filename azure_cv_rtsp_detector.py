#!/usr/bin/env python3
"""
Azure Custom Vision AI ONNX Model RTSP Stream Detector

This application uses an ONNX model exported from Azure Custom Vision AI
to detect and classify objects in real-time from an RTSP video stream.

Usage:
    python azure_cv_rtsp_detector.py --model <path_to_onnx_model> --rtsp <rtsp_url>

Requirements:
    - ONNX model exported from Azure Custom Vision AI
    - RTSP stream URL
    - Required Python packages (see requirements.txt)
"""

import argparse
import cv2
import numpy as np
import onnxruntime as ort
import time
import json
import sys
from typing import List, Tuple, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AzureCustomVisionDetector:
    """
    A class to handle ONNX model inference for Azure Custom Vision AI models.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the detector with an ONNX model.
        
        Args:
            model_path (str): Path to the ONNX model file
        """
        self.model_path = model_path
        self.session = None
        self.input_name = None
        self.output_names = []
        self.input_shape = None
        self.labels = []
        
        self._load_model()
    
    def _load_model(self):
        """Load the ONNX model and extract metadata."""
        try:
            # Create ONNX Runtime session
            self.session = ort.InferenceSession(self.model_path)
            
            # Get input details
            input_details = self.session.get_inputs()[0]
            self.input_name = input_details.name
            self.input_shape = input_details.shape
            
            # Get output details
            self.output_names = [output.name for output in self.session.get_outputs()]
            
            logger.info(f"Model loaded successfully: {self.model_path}")
            logger.info(f"Input shape: {self.input_shape}")
            logger.info(f"Input name: {self.input_name}")
            logger.info(f"Output names: {self.output_names}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            sys.exit(1)
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for Azure Custom Vision model.
        
        Args:
            image (np.ndarray): Input image in BGR format
            
        Returns:
            np.ndarray: Preprocessed image ready for inference
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Get target dimensions (assuming NCHW format: [batch, channels, height, width])
        if len(self.input_shape) == 4:
            target_height = self.input_shape[2]
            target_width = self.input_shape[3]
        else:
            # Default to common Azure Custom Vision dimensions
            target_height = target_width = 224
        
        # Resize image
        image_resized = cv2.resize(image_rgb, (target_width, target_height))
        
        # Normalize to [0, 1] range
        image_normalized = image_resized.astype(np.float32) / 255.0
        
        # Convert to NCHW format if needed
        if len(self.input_shape) == 4 and self.input_shape[1] == 3:
            image_normalized = np.transpose(image_normalized, (2, 0, 1))
        
        # Add batch dimension
        image_batch = np.expand_dims(image_normalized, axis=0)
        
        return image_batch
    
    def predict(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Run inference on the input image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            List[Dict[str, Any]]: List of predictions with labels and confidence scores
        """
        try:
            # Preprocess image
            input_data = self.preprocess_image(image)
            
            # Run inference
            outputs = self.session.run(self.output_names, {self.input_name: input_data})
            
            # Process outputs
            predictions = self._process_outputs(outputs)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return []
    
    def _process_outputs(self, outputs: List[np.ndarray]) -> List[Dict[str, Any]]:
        """
        Process model outputs to extract predictions.
        
        Args:
            outputs (List[np.ndarray]): Raw model outputs
            
        Returns:
            List[Dict[str, Any]]: Processed predictions
        """
        predictions = []
        
        try:
            # For classification models, typically the first output contains probabilities
            if len(outputs) > 0:
                probabilities = outputs[0][0]  # Remove batch dimension
                
                # Get top predictions
                top_indices = np.argsort(probabilities)[::-1]
                
                for i, idx in enumerate(top_indices):
                    confidence = float(probabilities[idx])
                    
                    # Only include predictions above a minimum threshold
                    if confidence > 0.1:  # 10% minimum confidence
                        predictions.append({
                            'label': f'Class_{idx}',  # Default label, can be customized
                            'confidence': confidence,
                            'class_id': int(idx)
                        })
                
        except Exception as e:
            logger.error(f"Error processing outputs: {e}")
        
        return predictions


class RTSPStreamProcessor:
    """
    A class to handle RTSP stream processing and video display.
    """
    
    def __init__(self, rtsp_url: str, detector: AzureCustomVisionDetector):
        """
        Initialize the RTSP stream processor.
        
        Args:
            rtsp_url (str): RTSP stream URL
            detector (AzureCustomVisionDetector): Detector instance
        """
        self.rtsp_url = rtsp_url
        self.detector = detector
        self.cap = None
        
    def connect(self) -> bool:
        """
        Connect to the RTSP stream.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            
            # Set buffer size to reduce latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to connect to RTSP stream: {self.rtsp_url}")
                return False
                
            logger.info(f"Successfully connected to RTSP stream: {self.rtsp_url}")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to RTSP stream: {e}")
            return False
    
    def process_stream(self, show_video: bool = True, save_results: bool = False):
        """
        Process the RTSP stream and run detection.
        
        Args:
            show_video (bool): Whether to display the video window
            save_results (bool): Whether to save detection results to file
        """
        if not self.connect():
            return
        
        frame_count = 0
        start_time = time.time()
        results_log = []
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    logger.warning("Failed to read frame from RTSP stream")
                    time.sleep(0.1)
                    continue
                
                frame_count += 1
                
                # Run detection every few frames to improve performance
                if frame_count % 5 == 0:  # Process every 5th frame
                    predictions = self.detector.predict(frame)
                    
                    # Log results
                    if predictions:
                        timestamp = time.time()
                        logger.info(f"Frame {frame_count}: {len(predictions)} detections")
                        
                        for pred in predictions:
                            logger.info(f"  {pred['label']}: {pred['confidence']:.3f}")
                        
                        if save_results:
                            results_log.append({
                                'timestamp': timestamp,
                                'frame': frame_count,
                                'predictions': predictions
                            })
                    
                    # Draw predictions on frame
                    if show_video:
                        frame = self._draw_predictions(frame, predictions)
                
                # Display frame
                if show_video:
                    cv2.imshow('Azure Custom Vision RTSP Detection', frame)
                    
                    # Break on 'q' key press
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Calculate and display FPS every 30 frames
                if frame_count % 30 == 0:
                    elapsed_time = time.time() - start_time
                    fps = frame_count / elapsed_time
                    logger.info(f"Processing FPS: {fps:.2f}")
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        
        except Exception as e:
            logger.error(f"Error during stream processing: {e}")
        
        finally:
            # Clean up
            if self.cap:
                self.cap.release()
            if show_video:
                cv2.destroyAllWindows()
            
            # Save results if requested
            if save_results and results_log:
                self._save_results(results_log)
    
    def _draw_predictions(self, frame: np.ndarray, predictions: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw prediction results on the frame.
        
        Args:
            frame (np.ndarray): Input frame
            predictions (List[Dict[str, Any]]): Prediction results
            
        Returns:
            np.ndarray: Frame with drawn predictions
        """
        height, width = frame.shape[:2]
        
        # Draw predictions text
        y_offset = 30
        for pred in predictions[:5]:  # Show top 5 predictions
            text = f"{pred['label']}: {pred['confidence']:.3f}"
            cv2.putText(frame, text, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            y_offset += 30
        
        # Draw timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def _save_results(self, results_log: List[Dict[str, Any]]):
        """
        Save detection results to a JSON file.
        
        Args:
            results_log (List[Dict[str, Any]]): Detection results
        """
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"detection_results_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(results_log, f, indent=2)
            
            logger.info(f"Results saved to: {filename}")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Azure Custom Vision AI ONNX Model RTSP Stream Detector'
    )
    parser.add_argument(
        '--model', '-m',
        required=True,
        help='Path to the ONNX model file exported from Azure Custom Vision AI'
    )
    parser.add_argument(
        '--rtsp', '-r',
        required=True,
        help='RTSP stream URL (e.g., rtsp://username:password@ip:port/stream)'
    )
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Run without displaying video window (headless mode)'
    )
    parser.add_argument(
        '--save-results',
        action='store_true',
        help='Save detection results to JSON file'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    logger.info("Starting Azure Custom Vision RTSP Detector")
    logger.info(f"Model: {args.model}")
    logger.info(f"RTSP URL: {args.rtsp}")
    
    try:
        # Initialize detector
        detector = AzureCustomVisionDetector(args.model)
        
        # Initialize stream processor
        processor = RTSPStreamProcessor(args.rtsp, detector)
        
        # Start processing
        processor.process_stream(
            show_video=not args.no_display,
            save_results=args.save_results
        )
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()