import cv2
import os
from datetime import datetime
import subprocess
import time

# Create a directory to save captured images
output_dir = "captured_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def run_scan_img():
    # Run the scan_img.py script and capture its output
    result = subprocess.run(
        ["python", "scan_img.py"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()  # Return the script's output as text

def run_scan_comp():
    # Run the scan_img.py script and capture its output
    result = subprocess.run(
        ["python3", "scan_comp.py"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()  # Return the script's output as text

'''

TEMP OMITTED BECAUSE RUNNING THIS PROCESS CURRENTLY REQUIRES MORE INPUT TOKENS THAN GPT API ALLOWS
-- That could change in the future however --

def save_to_comparison_folder(frame):
    """Save the current frame to the comparison_images folder."""
    comparison_dir = "comparison_images"
    if not os.path.exists(comparison_dir):
        os.makedirs(comparison_dir)

    # Create a unique filename using the current timestamp
    filename = datetime.now().strftime("comparison_%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(comparison_dir, filename)
    cv2.imwrite(filepath, frame)
    print(f"Image saved to comparison folder at {filepath}")

'''

def draw_ui_text(frame, text, box_height=0.20, margin=0.05, transparency=0.7):
    """Draws a semi-transparent rectangle and places dynamically wrapped text inside."""
    h, w, _ = frame.shape
    box_y_start = int(h * (1 - box_height))  # Start of the rectangle
    box_y_end = h

    # Calculate left and right margins
    left_margin = int(w * margin)
    right_margin = w - int(w * margin)

    # Draw the semi-transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, box_y_start), (w, box_y_end), (255, 255, 255), -1)
    cv2.addWeighted(overlay, transparency, frame, 1 - transparency, 0, frame)

    # Split text into dynamically wrapped lines
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Test adding the next word to the current line
        test_line = current_line + " " + word if current_line else word
        text_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
        if text_size[0] <= (right_margin - left_margin):  # Fits within the margins
            current_line = test_line
        else:  # Wrap to the next line
            lines.append(current_line)
            current_line = word
    if current_line:  # Add the last line
        lines.append(current_line)

    # Draw each line centered within the rectangle
    y = box_y_start + int((box_y_end - box_y_start) * 0.1)  # Start with padding
    for line in lines:
        text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
        x = left_margin + (right_margin - left_margin - text_size[0]) // 2  # Center align
        cv2.putText(frame, line, (x, y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
        y += text_size[1] + 10  # Move down for the next line

def main():
    # Open the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    #print("Press 'c' to capture an image, or 'q' to quit.")
    response_text = "Welcome to the Injury Scanner! Press 'c' to capture an image and receive an analysis of it, or 'q' to quit."

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        # Draw the UI text
        display_frame = frame.copy()
        draw_ui_text(display_frame, response_text)

        # Show the frame
        cv2.imshow('Camera', display_frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):  # 'c' key to capture
            # Create a unique filename using the current timestamp
            filename = datetime.now().strftime("image_%Y%m%d_%H%M%S.jpg")
            filepath = os.path.join(output_dir, filename)
            # Save the frame as an image file
            cv2.imwrite(filepath, frame)
            print(f"Image saved at {filepath}")

            # Update UI to show loading response
            response_text = "Loading response..."
            draw_ui_text(display_frame, response_text)
            cv2.imshow('Camera', display_frame)
            cv2.waitKey(1)  # Refresh UI

            # Run the scan_img.py script and get the response
            print("Running scan_img.py...")
            try:
                response_text = run_scan_img() + "\nPress 'c' to capture another image, or 'q' to quit."
                print("\n--- Scan Response ---")
                print(response_text)
            except Exception as e:
                response_text = f"Error during scan: {e}"
                print(response_text)

        elif key == ord('q'):  # 'q' key to quit
            print("Exiting.")
            break

        '''

        TEMP OMITTED BECAUSE RUNNING THIS PROCESS CURRENTLY REQUIRES MORE INPUT TOKENS THAN GPT API ALLOWS
        -- That could change in the future however --
        
        elif key == ord('x'):  # 'x' key to save to comparison_images
            save_to_comparison_folder(frame)
            response_text = "Image saved to comparison folder. Press 's' to analyze progression, or 'q' to quit."

        elif key == ord('s'):  # 's' key to analyze progression
            # Update UI to show loading response
            response_text = "Loading response..."
            draw_ui_text(display_frame, response_text)
            cv2.imshow('Camera', display_frame)
            cv2.waitKey(1)  # Refresh UI

            # Run the scan_img.py script and get the response
            print("Running scan_comp.py...")
            try:
                response_text = run_scan_comp() + "\nPress 'c' to capture another image, or 'q' to quit."
                print("\n--- Scan Response ---")
                print(response_text)
            except Exception as e:
                response_text = f"Error during progression analysis: {e}"
                print(response_text)

        '''

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
