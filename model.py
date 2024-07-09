import torch
from torch import nn
import torchvision
def create_effnet_b2(num_classes:int=101):
  #1
  weights=torchvision.models.EfficientNet_B2_Weights.DEFAULT
  transforms=weights.transforms()
  model=torchvision.models.efficientnet_b2(weights=weights).to('cpu')#gpu may or may not be available

  #2. freeze all parameters in all layers
  for param in model.parameters():
    param.requires_grad=False
  #3. set random seed
  seed=69
  
  torch.manual_seed(seed)
  torch.cuda.manual_seed(seed)
  #4. changing classifier layer
  model.classifier= torch.nn.Sequential(nn.Dropout(p=0.2, inplace=True),
                                        nn.Linear(in_features=1408,
                                                  out_features=num_classes,
                                                  bias=True).to('cpu'))
  #5. give name
  model.name='effnet_b2'
  print(f"Making EfficientNet_B2")

  return model,weights,transforms
