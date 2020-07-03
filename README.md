# Studley Winfield 2016

A recreation of the experiment described by Jones, Studley, Hauert & Winfield (2016) in _Evolving Behaviour Trees for Swarm Robotics_.

For tables, figures and equations please refer to the original paper.

This system is being implemented using ARGoS and DEAP and uses the ARGoS examples at https://github.com/ilpincy/argos3-examples as its basis.

## Task Specifications

* circular nest region separated from and surrounded by a food region
* robots placed at centre to start
* starting position is consistent but orientation is random
* fitness is correlated with the number of food items brought to the nest
* equation 1 describes maximum fitness
* equation 2 derates and normalises fitness
* bespoke simulator based on Box2D
* ten simulations for each individual
* twenty five robots in each simulation
* each simulation runs for 300 simulated seconds 

## Robot Specifications

* tick at 2Hz
* environment sensing at 8Hz averaged over seven samples
* forward velocity 8×10−3ms−1
* turn velocity 0.55rad s−1
* hardwired capabilities blackboard (table 1)
* robots can tell if they're moving towards or away from food or the nest by tracking distance over time
* distance calculated by tracking minimum communication hops (figure 2)
* message handling is asynchronous
* noise added to actuators

### Sensing
* read scratchpad
* signal received
* carrying food
* detecting food
* local density of other robots (equation 4)
* change in density of other robots (equation 4)
* distance over time to food / nest (figure 2)
 
### Actuation
* move forward, left or right
* write to scratchpad
* send signal

### Blackboard
* motors
* scratchpad
* send signal
* received signal
* detected food
* carrying food
* local density of robots
* change in density
* change in distance to food
* change in distance to nest

### Each cycle the following steps take place
1. New blackboard values are calculated based on the messages received and the environment. 
2. The behaviour tree is ticked, possibly reading and writing the blackboard. 
3. The movement motors are activated, and the message signal flag set according to the blackboard values.

## Behaviour Tree Specifications

* nodes shown in table 2
* composition node arity is between 2 and 4
* composition nodes resume execution from previous state instead of restarting
* maximum tree depth of 30 and number of nodes 140 (because of kilobot memory constraints)

#### Composition nodes: 
* select
* sequence
* probabilistic

#### Decorator nodes:
* repeat
* success
* failure

#### Condition nodes:
* less-than or greater-than-or-equal-to variable
* less-than or greater-than-or-equal-to constant
* success
* failure

#### Action nodes:
* move forward, left or right
* write to blackboard entry

## Evolutionary Specifications
* evolutionary parameters given in table 3
* 200 generations per run
* populations of 25 individuals
* tournament selection and elitism
* tree crossover and four mutation operators
* fittest individual over 25 populations is evaluated over 200 simulations
* then deployed to real robots and evaluated 20 times

### Mutation operators

* a node is selected at random and its subtree replaced with a randomly generated one
* a branch is chosen randomly and replaced with one of its terminals
* a node is picked at random and replaced with another node with the same argument types
* a constant is picked randomly and its value changed
