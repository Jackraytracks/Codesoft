import cv2
import face_recognition
import numpy as np

def load_known_faces():
    known_faces = {}
    known_images = ["person1.jpg", "person2.jpg"]  # Add image file names
    names = ["Alice", "Bob"]  # Corresponding names
    
    for img_path, name in zip(known_images, names):
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_faces[name] = encoding[0]
    
    return known_faces

def detect_and_recognize_faces(image_path, known_faces):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    recognized_faces = []
    for encoding, location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(list(known_faces.values()), encoding)
        name = "Unknown"
        
        face_distances = face_recognition.face_distance(list(known_faces.values()), encoding)
        best_match_index = np.argmin(face_distances) if matches else None
        
        if best_match_index is not None and matches[best_match_index]:
            name = list(known_faces.keys())[best_match_index]
        
        recognized_faces.append((name, location))
    
    return recognized_faces

def draw_faces(image_path, recognized_faces):
    image = cv2.imread(image_path)
    for name, (top, right, bottom, left) in recognized_faces:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    cv2.imshow("Face Recognition", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example Usage:
# known_faces = load_known_faces()
# recognized = detect_and_recognize_faces("test_image.jpg", known_faces)
# draw_faces("test_image.jpg", recognized)
