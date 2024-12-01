import cv2
import os
from datetime import datetime
import subprocess

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

def draw_multiline_text(frame, text, box_height=0.20, words_per_line=20, margin=0.05):
    """Draws a white rectangle at the bottom and places multiline text inside it."""
    h, w, _ = frame.shape
    box_y_start = int(h * (1 - box_height))  # Start of the white rectangle

    # Calculate the margins
    left_margin = int(w * margin)
    right_margin = w - int(w * margin)

    # Draw white rectangle
    cv2.rectangle(frame, (0, box_y_start), (w, h), (255, 255, 255), -1)

    # Split text into lines of approximately `words_per_line` words
    words = text.split()
    lines = [
        " ".join(words[i:i + words_per_line]) 
        for i in range(0, len(words), words_per_line)
    ]

    # Determine the maximum font scale to fit all lines in the box
    font_scale = 1
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        text_height_total = 0
        line_sizes = []

        for line in lines:
            text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
            line_sizes.append(text_size)
            text_height_total += text_size[1] + 10  # Add spacing between lines

        if text_height_total < h * box_height * 0.9 and all(
            size[0] <= (right_margin - left_margin) for size in line_sizes
        ):  # Ensure text fits within the box and respects margins
            break
        font_scale -= 0.1  # Decrease font size if too large

    # Draw each line centered within the rectangle, respecting margins
    y = box_y_start + (h - box_y_start - text_height_total) // 2  # Start at the center
    for line, text_size in zip(lines, line_sizes):
        text_width = text_size[0]
        x = left_margin + (right_margin - left_margin - text_width) // 2  # Center text within margins
        cv2.putText(
            frame,
            line,
            (x, y),
            font,
            font_scale,
            (0, 0, 0),  # Black text
            thickness,
            cv2.LINE_AA
        )
        y += text_size[1] + 10  # Move to the next line

def main():
    # Open the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    print("Press 'c' to capture an image, or 'q' to quit.")
    response_text = "Welcome to the Injury Scanner! Press 'c' to capture an image, or 'q' to quit."  # Default message

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        # Add the response text in a white rectangle at the bottom
        display_frame = frame.copy()
        draw_multiline_text(display_frame, response_text)

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

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
