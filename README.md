# alphantasy-hockey
Constructing a Neural RL Methodology to creating the ultimate fantasy hockey manager

Home of Victor Ardulov's and Fan Hung's official weekend project...

We will use python 3.8

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

make sure that your pip is the pip3.8


## Rules of the "Game"

Below we will describe the observable space, the action space, and the reward function of each agent. This is also the place to describe any time dependencies about how the system (i.e. how frequently can an agent make an action?)

1. **The Environment** - The environment consists of a number agents that compete in weekly head-to-head fantasy hocky match-ups. Each agent "manages" a team consisting of:
  * 2 active Centers (C)
  * 2 active Right Wings (RW)
  * 2 active Left Wings (LW)
  * 4 active Defensemen (D)
  * 2 Goalies (G)
  * 3 Bench slots
 for the purposes of this experiment we will ommit dealing with Injured Reserves (IR) which is actually commonly available.
 
2. **The Agents/Teams** - Each agent will be alotted a weekly amount of adds/drops and be required to set their line-up daily. For simplicity we will ommit trade offers and accepting for the time being

3. **The Reward** - In this league we will follow goals, assists, hits, and shots for forwards and defenseman and wins and saves for goalies. By accumulating the 


Initially let us begin by generating fake hockey data to make sure that the modelling can work as necessary and to iron out engineering issues that may arise.

## Modeling

Below we describe the methods that we use to implement the agents and their training methods.

## APIs 

Here we will put all of the APIs that are necessary for this to work effetively:
