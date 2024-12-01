# InjuryScanner

InjuryScanner is a Python-based application that captures images using a webcam, processes them to analyze potential medical conditions, and displays the analysis results in real-time.

## Features

- **Image Capture**: Utilize your webcam to capture images for analysis.
- **Medical Analysis**: Analyze captured images to identify potential medical issues and suggest possible treatments.
- **Real-Time Display**: Display analysis results directly on the screen immediately after capturing an image.

## Prerequisites

- Python 3.x
- OpenCV
- OpenAI Python Client
- dotenv

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Ryannasr11/InjuryScanner.git
   cd InjuryScanner

2. **Install Dependencies**:

    pip install -r requirements.txt

3. **Set Up Environment Variables**:

   - Create a `.env` file in the project directory.
   - Add your OpenAI API key to the `.env` file:

     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

1. **Run the Application**:

   ```bash
   python capture_img.py

2. **Capture an Image**:

   - Press the 'c' key to capture an image using your webcam.

3. **View Analysis**:

   - After capturing, the application will process the image and display the analysis results at the bottom of the screen.

4. **Exit**:

   - Press the 'q' key to quit the application.

## File Structure

- `capture_img.py`: Handles image capture and displays analysis results.
- `scan_img.py`: Processes the captured image and interacts with the OpenAI API for analysis.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenAI](https://www.openai.com/) for their API services.
- [OpenCV](https://opencv.org/) for the computer vision library.