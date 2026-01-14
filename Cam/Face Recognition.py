import cv2

# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the camera
cap = cv2.VideoCapture(1)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(
        gray,               # Input image
        scaleFactor=1.1,    # Scale factor for resizing during detection
        minNeighbors=5,     # Minimum number of neighbors for a detection
        minSize=(30, 30)    # Minimum size of detected faces
    )

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,          # Image to draw on
            (x, y),         # Top-left corner of the rectangle
            (x + w, y + h), # Bottom-right corner of the rectangle
            (0, 255, 0),    # Color of the rectangle (Green)
            2               # Thickness of the rectangle border
        )

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera resources and close display windows
cap.release()
cv2.destroyAllWindows()