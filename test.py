import cv2

# Create a VideoCapture object to capture video from the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error opening the camera")
    exit()

# Read and display video frames until the user quits
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # If the frame was not read successfully, end the loop
    if not ret:
        print("Failed to capture frame from camera")
        break

    # Display the frame in a window named "Video"
    cv2.imshow("Video", frame)

    # Wait for the user to press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()

