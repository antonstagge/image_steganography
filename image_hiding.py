import sys
import cv2
import numpy as np
import getopt

n = 2
AND_MASK = [-1, 254, 252, 248, 240, 224, 192, 128]
BIT_SHIFT = [-1, 7, 6, 5, 4, 3, 2, 1]
def encode(carrier_name, secret_name, output_name):
    carrier = cv2.imread(carrier_name)
    secret = cv2.imread(secret_name)
    hidden = np.ndarray(carrier.shape, dtype=int)

    for x in range(hidden.shape[0]):
        for y in range(hidden.shape[1]):
            for c in range(hidden.shape[2]):
                if x < secret.shape[0] and y < secret.shape[1]:
                    clean = carrier[x][y][c] & AND_MASK[n]
                    prepared = secret[x][y][c] >> BIT_SHIFT[n]
                    hidden[x][y][c] = clean | prepared
                else:
                    hidden[x][y][c] = carrier[x][y][c]

    cv2.imwrite(output_name, hidden, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])


def decode(hidden_name, output_name):
    hidden = cv2.imread(hidden_name)
    extracted = np.ndarray(hidden.shape, dtype=int)
    for x in range(hidden.shape[0]):
        for y in range(hidden.shape[1]):
            for c in range(hidden.shape[2]):
                extracted[x][y][c] = (hidden[x][y][c] & 255 - AND_MASK[n]) << BIT_SHIFT[n]
                
    cv2.imwrite(output_name, extracted, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

def decode_anim(hidden_name, output_name):
    hidden = cv2.imread(hidden_name)
    extracted = np.ndarray(hidden.shape, dtype=int)
    for i in range(0, (8-n)):
        for x in range(hidden.shape[0]):
            for y in range(hidden.shape[1]):
                for c in range(hidden.shape[2]):
                    extracted[x][y][c] = (hidden[x][y][c] << BIT_SHIFT[7-i]) & 255
                
        cv2.imwrite(str(i) + "_" + output_name, extracted, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

if __name__ == "__main__":
    argv = sys.argv[1:]
    carrier_name = ""
    secret_name = ""
    hidden_name = ""
    output_name = "output.png"
    anim = False

    try:
        if len(argv) == 0:
            raise ValueError("Not enough arguments")
        opts, args = getopt.getopt(argv,"c:s:d:n:o:a",["carrier=", "secret=", "decode=", "n=", "output=", "anim"])
    except Exception:
        print("To encode:\n python3 image_hiding.py -c carrier.png -s secret.png -o output.png -n bits\n")
        print("To decode:\n python3 image_hiding.py -d hidden.png -o output.png -n bits \n")
        sys.exit(2)   
    for opt, arg in opts:
        if opt in ('-c', '--carrier'):
            carrier_name = arg
        if opt in ('-s', '--secret'):
            secret_name = arg
        if opt in ('-d', '--decode'):
            hidden_name = arg
        if opt in ('-n', '--n'):
            n = int(arg)
            if n < 1 or n > 7:
                raise ValueError("Wrong n value!")
        if opt in ('-o', '--output'):
            if arg.split('.')[-1] != 'png':
                raise ValueError("Output has to by png!")
            output_name = arg
        if opt in ('-a', '--anim'):
            anim = True
    
    if not carrier_name == "" and not secret_name == "":
        encode(carrier_name, secret_name, output_name)
    elif not hidden_name =="" and anim:
        decode_anim(hidden_name, output_name)
    elif not hidden_name =="":
        decode(hidden_name, output_name)

    exit()