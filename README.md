# alphantasy-hockey
Constructing a Neural RL Methodology to creating the ultimate fantasy hockey manager

Home of Victor Ardulov's and Fan Hung's official weekend project...

We will use python 3.6 until `keras` and `tensorflow` wise up and support 3.7

Not an official partner of Google Deepmind OR the NHL... yet...

![As they say in hockey: "Let's do that hockey!"](https://media.giphy.com/media/l2QDYW7wm9CsU7DHO/giphy.gif)

## Getting Started

There are 2 options for getting started, but both of them require that you start with cloning this repo:

```git clone https://github.com/VArdulov/alphantasy-hockey.git```

*note:* you should consider making a seperate fork if you want to develop

Then you want to either create a conda environment and install the dependencies:

```conda env create --file environment.yaml```

Alternatively if you don't want to deal with environments and you have a global python 3.6 install

```pip install -r requirements.txt``` 

make sure that your pip is the pip3.6, tensorflow and keras don't work for 3.7 yet.


## Rules of the "Game"

Below we will describe the observable space, the action space, and the reward function of each agent. This is also the place to describe any time dependencies about how the system (i.e. how frequently can an agent make an action?)

## Modeling

Below we describe the methods that we use to implement the agents and their training methods.

## APIs 

Here we will put all of the APIs that are necessary for this to work effetively:
