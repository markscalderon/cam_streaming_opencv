import numpy as np
import cv2
import socket

UDP_IP = "172.43.1.28" ##local ip
UDP_PORT = 10000
ENCODE_QUALITY = 80
PACK_SIZE = 4096
FRAME_INTERNAL = (1000/30)
BUF_LEN = 65540

print("UDP target ip: ", UDP_IP)
print("UDP target port: ", UDP_PORT)

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
while(True):
    try:
        while(True):
            data , addr = sock.recvfrom(BUF_LEN)
            if(len(data) > 0 and len(data) < 3):
                break
        print(data)
        total_pack = int(data)
        print("expecting length of packs "+ data)

        dimg = ''

        for i in xrange(total_pack):
            img, addi = sock.recvfrom(BUF_LEN)
            simg = len(img)
            if( simg != PACK_SIZE):
                print("Received unexpected size pack: "+ str(simg))
            dimg = dimg + img
        un_image = np.fromstring(dimg, dtype = np.uint8)
        frame = cv2.imdecode(un_image, 1)

        if(frame.size == 0):
            print("decode failure")
            continue

        cv2.imshow('frame',frame)
        if( cv2.waitKey(1) & 0xFF == ord('q')):
            break

    except KeyboardInterrupt:
        print("Interruption")

cv2.destroyAllWindows()
sock.close()
