# Parking Space Detection System

A real-time computer vision application that monitors parking lot occupancy using video analysis. The system detects available and occupied parking spaces in a parking lot and updates the information to a Firebase Realtime Database.

## Overview

This project uses OpenCV and computer vision techniques to analyze parking lot video feeds and determine which parking spaces are free or occupied. The system allows users to define parking space boundaries interactively and then monitors those spaces in real-time, providing occupancy data that can be accessed remotely via Firebase.

## Technologies Used

### Core Technologies
- **Python** - Primary programming language
- **OpenCV (cv2)** - Computer vision library for image processing and analysis
- **NumPy** - Numerical computing for array operations and image manipulation
- **CVZone** - Computer vision helper library for simplified OpenCV operations

### Cloud Services
- **Firebase** - Real-time database for storing and sharing parking occupancy data
  - Firebase Admin SDK for Python integration
  - Firebase Realtime Database for live data synchronization

### Additional Libraries
- **Pickle** - Python object serialization for saving parking space coordinates

## Features

- **Interactive Parking Space Definition**: Use the picker tool to manually define parking space boundaries
- **Real-time Detection**: Monitors video feed and detects parking space occupancy
- **Adaptive Thresholding**: Adjustable parameters for different lighting conditions
- **Firebase Integration**: Uploads occupancy data to cloud database in real-time
- **Visual Feedback**: Displays parking spaces with color-coded status (green for free, red for occupied)
- **Space Numbering**: Each parking space is numbered for easy identification

## Project Structure

```
ObjectDetection/
├── main.py                    # Main application - runs parking space detection
├── picker.py                  # Interactive tool to define parking space coordinates
├── carPark.mp4               # Video feed of the parking lot
├── carParkImg.png            # Reference image of the parking lot
├── CarCoordinates            # Pickled file storing parking space boundary coordinates
├── CarParkPos                # Additional position data
├── parking-system-*.json     # Firebase credentials (keep these secure!)
└── .idea/                    # PyCharm/IntelliJ IDE configuration
```

## Setup Instructions

### Prerequisites
- Python 3.x installed
- Webcam or video file of a parking lot

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aarogyarijal/ObjectDetection.git
cd ObjectDetection
```

2. Install required Python packages:
```bash
pip install opencv-python opencv-contrib-python numpy cvzone firebase-admin
```

3. Configure Firebase:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Realtime Database
   - Download your Firebase Admin SDK credentials JSON file
   - Replace the credentials file path in `main.py` (line 8)
   - Update the database URL in `main.py` (line 10)

## Usage

### Step 1: Define Parking Spaces

Run the picker tool to interactively define parking space boundaries:

```bash
python picker.py
```

- **Left Click**: Mark the four corners of each parking space (click 4 times per space)
- **Right Click**: Remove the last defined parking space
- The coordinates are automatically saved to `CarCoordinates` file

### Step 2: Run the Detection System

Start the main application to monitor parking spaces:

```bash
python main.py
```

The system will:
- Load the parking space coordinates from `CarCoordinates`
- Process the video feed frame by frame
- Detect occupancy for each parking space
- Display the results with visual indicators
- Upload occupancy data to Firebase in real-time

### Adjusting Detection Parameters

The application provides trackbars to fine-tune detection parameters:
- **Val1**: Adaptive threshold block size (affects edge detection)
- **Val2**: Adaptive threshold constant (fine-tunes threshold value)
- **Val3**: Median blur kernel size (reduces noise)

Adjust these values in real-time to optimize detection for different lighting conditions.

## How It Works

1. **Video Processing**: Captures frames from the parking lot video
2. **Image Preprocessing**: 
   - Converts to grayscale
   - Applies Gaussian blur to reduce noise
   - Uses adaptive thresholding for edge detection
   - Applies median blur and dilation for better contours
3. **Space Analysis**: For each defined parking space:
   - Crops the region of interest
   - Counts non-zero pixels (white pixels after thresholding)
   - Determines occupancy based on pixel count threshold
4. **Data Reporting**: Updates Firebase with current occupancy status
5. **Visual Display**: Shows processed images and parking space status

## Firebase Data Structure

The system updates Firebase with the following data structure:

```json
{
  "occupancy": [
    {"slot": 1, "state": "free"},
    {"slot": 2, "state": "occupied"},
    {"slot": 3, "state": "free"}
    // ... more parking spaces
  ]
}
```

## Security Note

⚠️ **Important**: The Firebase credentials JSON files contain sensitive information. Never commit these files to public repositories. Add them to `.gitignore` to prevent accidental exposure.

## Future Enhancements

- Add support for live camera feeds
- Implement automated parking space detection using deep learning
- Create a web dashboard to visualize parking occupancy
- Add historical data analysis and reporting
- Implement alerts for parking lot capacity thresholds

## License

This project is available for educational and personal use.

## Author

Aarogya Rijal - [GitHub Profile](https://github.com/aarogyarijal)
