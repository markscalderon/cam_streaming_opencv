import numpy as np
import cv2
import socket

### based on https://github.com/chenxiaoqino/udp-image-streaming

UDP_IP = "127.0.0.1"
UDP_PORT = 10000
ENCODE_QUALITY = 80
PACK_SIZE = 4096
FRAME_INTERNAL = (1000/30)

print("UDP target ip: ", UDP_IP)
print("UDP target port: ", UDP_PORT)

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    flag, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, ENCODE_QUALITY])
    if False == flag:
        print('cloud not encode image')
        break

    total_pack = 1 + (encoded.size - 1) / PACK_SIZE;
    ibuf = str(total_pack)

    sock.sendto(ibuf,(UDP_IP,UDP_PORT))

    for i in xrange(total_pack):
        sock.sendto(encoded[i*PACK_SIZE: (i+1)*PACK_SIZE ].tostring(),(UDP_IP,UDP_PORT))
    cv2.imshow('image', frame)
    if cv2.waitKey(FRAME_INTERNAL) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
sock.close()
