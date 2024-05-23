import cv2
from transformers import pipeline
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from stereFlow import genStereFlow,warpFlow
import pdb
from tqdm import tqdm
import gradio as gr


def video2video(filename, drate = 2, scale = 10):
    outfile = filename + '.avi'
    
    cap = cv2.VideoCapture(filename)

    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    drate = int(drate)

    h2 = h//drate
    w2 = w//drate

    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    videoWriter = cv2.VideoWriter(filename + '.avi', fourcc, 25, (w2*2, h2))

    for i in tqdm(range(cnt)):
        ret, frame = cap.read()

        if frame is None:
            break
        frame = cv2.resize(frame,(w2,h2))
        image = Image.fromarray(frame[:,:,::-1])

        depth = pipe(image)["depth"]
        depth =np.array(depth).astype(np.float32)/255.0
        depth = cv2.medianBlur(depth, 5)

        disp = scale*depth[:,:]

        left_offset, right_offset = genStereFlow(disp)
        left_offset = cv2.medianBlur(left_offset, 5)
        right_offset = cv2.medianBlur(right_offset, 5)

        left_img = warpFlow(frame, left_offset)
        right_img = warpFlow(frame, right_offset)

        du_image = np.concatenate((left_img, right_img), 1)
        videoWriter.write(du_image)

    cap.release()
    videoWriter.release()
    
    return outfile

pipe = pipeline(task = "depth-estimation", model="LiheYoung/depth-anything-small-hf", device="cuda")

inputs = gr.Video()
outputs = gr.Video(label="输出视频")

downsample = gr.Slider(1,4, value = 4, label="Downsample")
scale = gr.Slider(1,20, value = 10, label="Dispasity Scale")

demo = gr.Interface(fn = video2video, inputs = [inputs, downsample, scale], outputs = outputs)
demo.launch(server_name='0.0.0.0')#share=True)
