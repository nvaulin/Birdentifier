import os
import random
import imagehash
import numpy as np
from PIL import Image
import seaborn as sns
from datetime import datetime
from glob import glob
from IPython.display import clear_output
import pickle
import torch
from torch import nn
from torch.nn import functional as F
import torchvision
from torchvision import models, transforms
from torchvision.io import read_image
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import Compose, ToPILImage, Resize, ToTensor, Normalize

IMG_SIZE = 224, 224
DEVICE =  "cpu"

vgg_dict = pickle.load(open(os.path.join('birds_data', 'weights', "vgg19.pickle"), "rb"))
mdl3 = torchvision.models.vgg19_bn(pretrained=False)
num_features = 25088
mdl3.classifier = nn.Linear(num_features, 525)
mdl3 = mdl3.to(DEVICE)
mdl3.load_state_dict(torch.load(os.path.join('birds_data', 'weights', 'vgg19_bn.pth'), map_location=torch.device('cpu')))
mdl3.eval()

preprocessor = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


with open(os.path.join('messages', 'danya_messages.txt'), 'r') as file:
    danya_messages = file.read().splitlines()



def classify_with_vgg19(img):
    img = preprocessor(img)  
    img = img.unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        prediction = mdl3(img)
    _, predicted_class = torch.max(prediction, 1)
    return vgg_dict[int(predicted_class)]

def identify_class(picture_path, model=None):
    if find_similar_danya(picture_path):
        return random.choice(danya_messages)
    img = Image.open(picture_path)
    bird_name  = classify_with_vgg19(img)
    os.remove(picture_path)
    return f'Спасибо за птичку! Похоже это {bird_name}'

def find_similar_danya(image_path,similarity=80, hash_size=8):
    '''
    Function for comparing a photo with known Daniil Litvinov photos
    Was inspired by the https://github.com/cw-somil/Duplicate-Remover
    '''
    fnames = os.listdir(os.path.join('birds_data', 'danya'))
    threshold = 1 - similarity/100
    diff_limit = int(threshold*(hash_size**2))

    with Image.open(image_path) as img:
        hash1 = imagehash.average_hash(img, hash_size).hash

    for image in fnames:
        with Image.open(os.path.join(os.path.join('birds_data', 'danya'),image)) as img:
            hash2 = imagehash.average_hash(img, 8).hash
            if np.count_nonzero(hash1 != hash2) <= diff_limit:
                return True
    return False