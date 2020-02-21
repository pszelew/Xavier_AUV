# Neural network in Xavier_AUV
Here are all necessary informations about neural networks used in 
Xavier_AUV

## Folder structure
'''
├── DarknetClient.py        -> Client class that is used by different modules that need neural networks
├── DarknetServer.py        -> Server with clients are communicating 
├── models                  -> Catalog that contains trained models
│   └── gate                -> Example model structure
│       ├── yolo.cfg
│       ├── yolo.data
│       ├── yolo.names
│       └── yolo.weights
└── utils                   -> Utils used by server
    ├── darknet.py          -> Python wrapper for yolo (originally implemented in C)
    └── DarknetYoloModel.py -> Class with defines yolo model and implements required mothods
'''

## Model structure
'''
gate            
  ├── yolo.cfg
  ├── yolo.data
  ├── yolo.names
  └── yolo.weights
'''
dir name -> name of model, for example "gate"
yolo.cfg -> yolo neural network config, predefined. Include image sizes, number of classes etc.
yolo.data -> informations about how many classes are in model, contains path to yolo.names
yolo.names -> in this file are all classes names each in new line for example: "gate"
yolo.weights -> file that contains trained classes weights

## Usage

1. First check path to libdarknet.so in utils.darknet.py
⋅⋅⋅ libdarknet.so is in folder that contains compiled yolo neural networks
2.

todo ...

