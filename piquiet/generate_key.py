from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import json


def key_from_image(path="sample_image.jpg"):
    im = Image.open(path)
    shape = np.array(im).shape
    key = np.product(np.array(im).reshape(np.product(shape)).shape)
    d = {"key": int(key)}
    with open('private.key', 'w') as f:
        json.dump(d, f)
    return key


if __name__ == "__main__":
    key_from_image()