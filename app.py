import gradio as gr
import os
import torch
from model import create_effnet_b2
from PIL import Image
from timeit import default_timer as timer
from typing import Tuple, Dict
import pickle

#setup class names
#unpickle data from file 'train_classes.pkl' and assign it to variable name class_names
with open('train_classes.pkl','rb') as f:
  class_names=pickle.load(f)

###prepare model and transforms###

#create effnetb2
eff_net_b2,eff_net_b2_weights,eff_net_b2_transforms=create_effnet_b2(num_classes=len(class_names))

#load saved weights
eff_net_b2.load_state_dict(torch.load(f='pretrained_eff_net_feature_extractor.pth',map_location=torch.device('cpu'))) #loading to cpu as gpu might not be available in all devices where model is used


###Create Predict function###

def predict(img)->Tuple[Dict,float]:
  #start timer
  start_time=timer()
  #transform image
  img=eff_net_b2_transforms(img).unsqueeze(0)
  #put model in eval mode
  eff_net_b2.eval()
  with torch.inference_mode():
    #pass image through model
    pred_logits=eff_net_b2(img)
    #get prediction probability
    pred_prob=torch.softmax(pred_logits,dim=1)
    #get prediction label
    pred_label=torch.argmax(pred_prob,dim=1)

    #make a dictionary of class name and corresponding prediction probability of the class
    prob_dict={class_names[i]:pred_prob[0][i].item() for i in range(len(class_names))}

    #end timer and calculate time
    end_time=timer()
    time_elapsed=round(end_time-start_time,4)

  #return the dictionary and time
  return prob_dict, time_elapsed



###Gradio App##

#create title, description and articles
title="Food Prediction"
description='Takes an image as input and classifies it into sushi, pizza or steak'
article="Created in colab, github link:https://github.com/FrodoBaggins87/Machine_Learning/blob/main/Model_Deployment.ipynb"

#create example list
#example_list=[['examples/'+ example] for example in os.listdir('demo/food_prediction/examples')]

#create gradio interface
demo=gr.Interface(fn=predict,
                 inputs=gr.Image(type='pil'),
                 outputs=[gr.Label(num_top_classes=5,label='Prediction'),
                          gr.Number(label='Time Elapsed')],#Have to add examples here
                 title=title,
                 description=description,
                 article=article)

#launch demo (also putting server name and port name)
if __name__=="__main__":
  demo.launch(server_name='0.0.0.0', server_port=80, debug=False,share=True)
