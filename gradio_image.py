import cv2
from transformers import pipeline
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from stereFlow import genStereFlow,warpFlow
import pdb
from tqdm import tqdm
import gradio as gr


def image2image(image, drate = 2, scale = 10):
    
    depth = pipe(Image.fromarray(image))["depth"]
    depth =np.array(depth).astype(np.float32)/255.0
    depth = cv2.medianBlur(depth, 5)

    disp = scale*depth[:,:]

    left_offset, right_offset = genStereFlow(disp)
    left_offset = cv2.medianBlur(left_offset, 5)
    right_offset = cv2.medianBlur(right_offset, 5)

    left_img = warpFlow(image, left_offset)
    right_img = warpFlow(image, right_offset)

    du_image = np.concatenate((left_img, right_img), 1)

    return Image.fromarray(du_image)

pipe = pipeline(task = "depth-estimation", model="LiheYoung/depth-anything-small-hf", device="cuda")

inputs = gr.Image()
outputs = gr.Image(label="输出图片")

downsample = gr.Slider(1,4, value = 4, label="Downsample")
scale = gr.Slider(1,20, value = 10, label="Dispasity Scale")

demo = gr.Interface(fn = image2image, inputs = [inputs, downsample, scale], outputs = outputs)
demo.launch(server_name='0.0.0.0')#share=True)
