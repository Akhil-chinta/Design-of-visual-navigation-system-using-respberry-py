import socket
import numpy as np
import cv2 as cv


addr = ("192.168.43.22", 8000)
buf = 1024
width = 640
height = 480
code = b'start'
num_of_chunks = width * height * 3 / buf

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    
    while True:
        chunks = []
        start = False
        while len(chunks) < num_of_chunks:
            chunk, _ = s.recvfrom(buf)
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)

        frame = np.frombuffer(
            byte_frame, dtype=np.uint8).reshape(height, width, 3)

        cv.imshow('recv', frame)
        key = cv. waitKey(1)
        if key == ord('s'):
            
            cv.imwrite("C:/Users/Jayanth/Desktop/DCGAN-Based Data Augmentation for Tomato Leaf Disease Identification/testpicture/saved.jpg", frame)
            pass
        elif key == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()
