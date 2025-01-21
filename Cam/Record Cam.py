import cv2

# Video settings
width = 640
height = 480
fps = 30.0

# Initialize webcam capture object
capture = cv2.VideoCapture(0)

# Set video configurations
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
capture.set(cv2.CAP_PROP_FPS, fps)

# Define the video codec and the recording object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video.avi', fourcc, fps, (width, height))

while True:
    # Read the next frame from the webcam
    ret, frame = capture.read()

    if ret:
        # Write the frame to the video file
        out.write(frame)

        # Display the captured frame in real-time
        cv2.imshow("Webcam", frame)

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
capture.release()
out.release()
cv2.destroyAllWindows()
