# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 18:12:43 2020

@author: samwh


Section 1: Class to construct and manipulate keras models
Section 2: General functions required for new network interface
Section 3: Classes to allow for creation of sparse pseudo-networks

Notes:
    - NeuralNet objects updated to allow for use of different activation and
    optimizer functions. Currently this can only be changed for the entire
    model rather than individual layers.
    - Currently no functionality to allow for dropout layer, but this could be
    implemented if needed.
"""

import random
import numpy as np
import matplotlib.pyplot as plt

import keras
from keras.models     import Sequential
from keras.layers     import Dense
from keras.models     import load_model


# lists containing model activations and optimizers to allow for randomisation
hidden_layer_activations = ['tanh', 'relu', 'sigmoid', 'linear', 'softmax']
model_optimizers = ['adam', 'rmsprop']


###############################################################################


'''
Class to define Neural Net object, capable of loading an existing network from a .h5 file:
    network_name = NeuralNet(file="Neural_Network.h5") 

OR training a new network from a 'training_data' array with specified 'architecture' (layer structure):
    network_name = NeuralNet(training_data=array_name, architecture=[10,10,10]) 

OR creating an untrained neural net with specified 'input_size', 'output_size' and 'architecture':
    network_name = NeuralNet(input_size=4, output_size=2, architecture=[10,10,10])

Function overview:
    - To train a model, call 'fit(training_data)' where training_data is a list of inputs and outputs
    - Network can be saved to a .h5 file by calling the 'save(file_name)' method
    - To make a prediction, call 'predict(input_data)' method where input_data is an array of observations
    - Stored network architecture can be updated (e.g. after mutation) by calling 'get_architecture()' method
    - Return lists containing network weights and biases by calling 'get_weights()' (also updates internal variables)
    - Set network weights by calling 'set_weights(weights, biases)', input same data format as get_weights() output
'''

class NeuralNet():
    
    def __init__(self, 
                 file=None, 
                 architecture=None, 
                 input_size=None, 
                 output_size=None, 
                 training_data=None,
                 training_epochs=1,
                 activation='sigmoid',
                 optimizer='adam'
                 ):
        
        def build_model(input_size, output_size, architecture, activation, optimizer):
            
            model = Sequential()
            
            if len(architecture) > 0:
            
                model.add(Dense(architecture[0], input_dim=input_size, activation=activation))
                for i in range(1, len(architecture)):
                    model.add(Dense(architecture[i], activation=activation))
                model.add(Dense(output_size, activation='linear'))
                
            else: model.add(Dense(output_size, input_dim=input_size, activation='linear'))
            
            model.compile(loss='mse', optimizer=optimizer)
           
            return model

        if training_data: input_size, output_size = len(training_data[0][0]), len(training_data[0][1])
        
        if file:
            
            self.model = load_model(file)
            print('Loaded ' + file, '\n')
            
        else: self.model = build_model(input_size, output_size, architecture, activation, optimizer)
        
        if training_data: self.fit(training_data, training_epochs)
        
        self.get_architecture()
        self.get_weights()
        self.activation, self.optimizer = activation, optimizer
        
    
    # fits model to given training data    
    def fit(self, training_data, epochs=10):
            
        inputs = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
        outputs = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
        self.model.fit(inputs, outputs, epochs=epochs)
            
    
    # saves network inc. weights to a .h5py file with a given name
    def save(self, name='Neural_Network'):
        
        self.model.save(name + '.h5')
        print('Saved to {}'.format(name + '.h5'), '\n')
        
    
    # use the model to generate an output from a given input
    def predict(self, input_data):
        
        return self.model.predict(np.array(input_data).reshape(-1, len(input_data)))[0]
    
    
    # returns architecture (hidden layer structure) of network, also updates internal variables
    def get_architecture(self):
        
        architecture = []
        for layer in self.model.layers: architecture.append(layer.output_shape[1])
        
        self.output_size = architecture[-1]
        architecture.pop()
        self.architecture = architecture
        
        return architecture
    
    
    # outputs weights and biases of network, also updates internal variables
    def get_weights(self, _print=False):    
    
        weights, biases = [], []
        for layer in self.model.layers:
            weights.append(layer.get_weights()[0])
            biases.append(layer.get_weights()[1])
        
        if _print: print('Weights:', weights, '\n\nBiases:', biases, '\n')
        
        self.weights, self.biases = weights, biases
        self.input_size = len(weights[0])
        
        return weights, biases
    
    
    # accepts lists containing weights and biases and uses these to replace existing network weights
    def set_weights(self, weights, biases):
        
        count = 0
        for layer in self.model.layers:
            layer.set_weights([weights[count], biases[count]])
            count += 1
            
        self.get_weights()
    

###############################################################################
        
        
'''
Generic functions to be used by later methods:
    - Function to reset all weights to zero
    - Function to add a node with given weight
    - Function to delete a node
'''

# function to take arrays for weights and biases and set all values to zero
def set_zero_weights(weights, biases):

    # set weights values
    for layer in range(len(weights)):
        for node in range(len(weights[layer])):
            for connection in range(len(weights[layer][node])): weights[layer][node][connection] = 0
      
    # set bias values          
    for layer in range(len(biases)):
        for node in range(len(biases[layer])): biases[layer][node] = 0
    
    return weights, biases


# function to handle adding a given number ('diff') of nodes to a network architecture
# accepts the weights, biases and architecture of a network, the layer which the nodes will be added to
# the number of new nodes 'diff' and a bool to allow for randomising new node connection weights
def add_node(weights, biases, architecture, layer, diff=1, rand=False):
    
    # subfunction returns zero unless rand=True, in which case returns a random number from -1 to 1
    def new_val():
        
        if rand: return 2*random.random() - 1
        else: return 0
    
    # ensure diff is always positive
    if diff < 0: diff = -diff
    
    # add nodes to architecture    
    architecture[layer] += diff
    
    # handle addition of weights into the new nodes    
    new_layer = []
    for i in range(len(weights[layer])):
        l = [elem for elem in weights[layer][i]]
        for j in range(diff): l.append(new_val())
        new_layer.append(np.array(l))
    
    weights[layer] = np.array(new_layer)
    
    # handle addition of weights out of the new nodes 
    new_layer = []
    for i in range(len(weights[layer+1])): new_layer.append(np.array([elem for elem in weights[layer+1][i]]))
    for i in range(diff): new_layer.append(np.array([new_val() for j in range(len(weights[layer+1][0]))]))
    
    weights[layer+1] = np.array(new_layer)
    
    # new biases are always set to zero
    biases[layer] = np.append(biases[layer], [0 for i in range(diff)]) 
    
    return weights, biases, architecture


# handles deletion of a given number 'diff' of nodes from a specified layer 
def del_node(weights, biases, architecture, layer, diff=-1):
    
    # ensure diff is always negative
    if diff > 0: diff = -diff
    
    # delete nodes from architecture
    architecture[layer] += diff
    
    # delete associated weights and biases
    weights[layer] = np.delete(weights[layer], [len(weights[layer][0]) - 1 - i for i in range(abs(diff))], 1)
    weights[layer+1] = np.delete(weights[layer+1], [len(weights[layer+1]) - 1 - i for i in range(abs(diff))], 0)
    
    biases[layer] = np.delete(biases[layer], [len(biases[layer]) - 1 - i for i in range(abs(diff))])
    
    return weights, biases, architecture

def delete_link(connection):    
    node1, node2 = connection.vector
    
    if node2 in node1.input_conn: 
        node1.input_conn.remove(node2)
    elif node1 in node2.input_conn:
        node2.input_conn.remove(node1)
        
    elif node2 in node1.output_conn:
        node1.output_conn.remove(node2)
    elif node1 in node2.output_conn:
        node2.output_conn.remove(node1)
        
        
    node1.forward_conn.remove(node2)
    node2.back_conn.remove(node1)   
    # node2.forward_conn.remove(node1)
    # node1.back_con.remove(node2)
    node1.connection_genes.remove(connection)
    node2.connection_genes.remove(connection)
###############################################################################
  
                                   
    
'''
Classes for use in creating a 'pseudo-network', which can be sparsely rather than densely connected:
    - Connections between nodes are stored as ConnectionGene objects
    - Nodes are stored as NodeGene objects
    - Networks are stored as Chromosome objects, which take connection and node genes as arguments
    
Create a node as follows (layers are number in range [0,1], where 0,1 are input/ouput layers):
    node = NodeGene(bias=0, num=1, layer=0)
    
Connect two nodes and create a connection gene (cannot be in same layer):
    connection = node.add_connection(other_node, weight=0.5)
    
Create a chromosome:
    chromosome = Chromosome(connection_genes=[#list of connection genes#]
                            node_genes=[#list of node genes#]
                            )
                            
Compile genetic information into a keras model:
    model = chromosome.compile_network()
'''

# define object to contain information relating to a connection between nodes
class ConnectionGene():
    
    def __init__(self, weight=0, vector=[], innovation=None, activated=True):
        
        self.weight = weight
        self.vector = vector
        self.innovation = innovation
        self.activated = activated
        
        
# object to store information relating to a node in the network
# both node genes and connection genes can be 'turned off' by setting activated=False
# layer number must be in range [0,1] where 0 = input layer, 1 = output layer
class NodeGene():
    
    def __init__(self, 
                 bias,
                 num,                           # each node has an associated reference number
                 layer,                         # in range [0,1]
                 innovation=None,               # for use in NEAT
                 activated=True,                # set to False to deactivate gene
                 
                 # the below are not necessary for initialisation
                 eff_layer=None, 
                 eff_node_index=None,
                 forward_conn=[],
                 back_conn=[],
                 input_conn=[],
                 output_conn=[],
                 connection_genes=[]
                 ):

        if layer == 0: 
            eff_layer = 0
            self.type = 'input'
        elif layer == 1: 
            eff_layer = -1
            self.type = 'output'
        else:
            self.type='hidden'
        self.bias = bias
        self.num = num
        self.layer = layer
        self.innovation = innovation
        self.activated = activated
        
        
        self.eff_layer = eff_layer
        self.eff_node_index = eff_node_index
        self.forward_conn, self.back_conn = [], []
        self.input_conn, self.output_conn = [], []
        self.connection_genes = connection_genes

    
    # prints node connections if _print=True, returns lists of reference numbers of connected nodes
    def get_connections(self, _print=True):
        
        if _print:
            
            if self.layer == 0: _type = 'input'
            elif self.layer == 1: _type = 'output'
            else: _type = 'hidden'
            
            print('Node {}: (type={})'.format(self.num, _type))                   
            print('Forward connections:', [n.num for n in self.forward_conn])
            print('Backward connections:', [n.num for n in self.back_conn])
            print('layer', self.layer,'\n')
            
        return [n.num for n in self.forward_conn], [n.num for n in self.back_conn]
        
    
    # call this function to add a connection to another node (must be in a different layer)
    # returns a connection gene object
    def add_connection(self, other, weight=0, innovation=None, activated=True):
        
        if self.layer == other.layer: 
            # print('Tried to connect two nodes in same layer.\n')
            return None
        
        elif other in self.back_conn or other in self.forward_conn:
            # print('Connection already exists')
            return None 
        
        ### HMMM
        else:
            
            if self.layer < other.layer:
             
                self.forward_conn.append(other)
                other.back_conn.append(self)
                
                vector = [self, other]
                
            elif self.layer > other.layer:
                
                self.back_conn.append(other)
                other.forward_conn.append(self)
                
                vector = [other, self]
            
            # creates a new connection gene and adds it to lists for both nodes
            new_connection = ConnectionGene(weight=weight, vector=vector, innovation=innovation, activated=activated)
            
            self.connection_genes.append(new_connection)
            other.connection_genes.append(new_connection)
            
            return new_connection


# class to store genetic information of an object, as well as model information and fitness
# model can be generated from node and connection genes by calling the compile_network function
class Chromosome():
    
    def __init__(self, 
                 model=None,                    # NeuralNet object
                 fitness=None,                  # fitness value
                 connection_genes=[],         # ConnectionGene objects
                 node_genes=[],               # NodeGene objects
                 architecture=[],
                 input_size=None, 
                 output_size=None,
                 activation='sigmoid',              
                 optimizer='adam'
                 ):
        
        self.model, self.fitness = model, fitness
        self.connection_genes, self.node_genes = connection_genes, node_genes
        self.architecture = architecture
        self.input_size, self.output_size = input_size, output_size
        self.activation, self.optimizer = activation, optimizer
        # self.input_size = 4
        # self.output_size = 2
    
    # function to compile a keras model from the connection and node genes of the chromosome
    # saves model to object attributes and also returns the new model
    def compile_network(self):
    
        # find input and output sizes from node gene list
        if not self.input_size: self.input_size = len([n for n in self.node_genes if n.layer == 0])
        if not self.output_size: self.output_size = len([n for n in self.node_genes if n.layer == 1])
        
        architecture = []
        current_layer = []
        current_eff_layer = 1
        current_eff_node_index = 0
        
        # remove any deactivated genes
        connection_genes = [c for c in self.connection_genes if c.activated == True]
        node_genes = [n for n in self.node_genes if n.activated == True]
        
        # remove connection genes if they reference a deactivated or non-existent node
        temp = [c for c in connection_genes]
        for c in temp: 
            if c.vector[0] not in node_genes or c.vector[1] not in node_genes:
                del connection_genes[connection_genes.index(c)]
        
        # remove duplicate connections in list, taking only the most recently added connection gene
        temp = [c for c in connection_genes]
        for c in temp: 
            if c.vector in [x.vector for x in connection_genes[connection_genes.index(c)+1:]]: 
                del connection_genes[connection_genes.index(c)]
                
        temp = [n for n in node_genes]
        for n in temp:
            if n not in [c.vector[0] for c in connection_genes] + [c.vector[1] for c in connection_genes]:
                if n.layer not in [0,1]: del node_genes[node_genes.index(n)]
        
        # iterate through node genes to generate an architecture with layers of unconnected nodes
        node_genes.sort(key=lambda x: x.layer)
        for node_gene in (n for n in node_genes if n.layer not in [0,1]):
            
            # if node connected to current layer, move to next layer
            connected_to_layer = False
            for n in node_gene.back_conn: 
                if n in current_layer: connected_to_layer = True
            
            if connected_to_layer:
    
                architecture.append(len(current_layer))
                current_layer = []
                current_eff_layer += 1
                current_eff_node_index = 0
                
            current_layer.append(node_gene)
            node_gene.eff_layer = current_eff_layer
            node_gene.eff_node_index = current_eff_node_index
            current_eff_node_index += 1     
            
        # set node indices for input and output nodes
        for i in range(2):
            count = 0
            for n in (n for n in node_genes if n.layer == i): 
                n.eff_node_index = count
                count += 1
                if i == 0: n.eff_layer = 0
                elif len(current_layer) == 0: n.eff_layer = 1
                else: n.eff_layer = current_eff_layer + 1
            
        if len(current_layer) > 0: architecture.append(len(current_layer))
        
        # get shapes of weight and bias arrays
        temp_network = NeuralNet(None, architecture, self.input_size, self.output_size)
        weights, biases = temp_network.get_weights()
        weights, biases = set_zero_weights(weights, biases)
        
        # add all connection weights for adjacent layers
        for c in (c for c in connection_genes if c.vector[1].eff_layer - c.vector[0].eff_layer == 1):
            weights[c.vector[0].eff_layer][c.vector[0].eff_node_index][c.vector[1].eff_node_index] = c.weight

        # iterate through all node genes to add biases and remaining weights
        node_genes.sort(key=lambda x: x.layer, reverse=True)
        for node_gene in node_genes:
            
            # set bias value for node
            if node_gene.layer != 0: 
                biases[node_gene.eff_layer-1][node_gene.eff_node_index] = node_gene.bias
            
            # iterate through backwards node connections that span greater than one effective layer
            for n in (n for n in node_gene.back_conn if node_gene.eff_layer - n.eff_layer > 1):              
                for layer in range(n.eff_layer, node_gene.eff_layer - 1):
                    
                    # add new node to layer with weights of 0
                    weights, biases, architecture = add_node(weights, biases, architecture, layer)                
                    
                    # connect new node to original node with weight of 1
                    if layer == n.eff_layer: weights[layer][n.eff_node_index][-1] = 1
                    else: weights[layer][-1][-1] = 1
                    
                    # connect the new pathway to the final node with the original connection weight
                    if layer == node_gene.eff_layer - 2: 
                        
                        connection_gene = [c for c in node_gene.connection_genes if c.vector == [n, node_gene]][0]
                        weights[layer+1][-1][node_gene.eff_node_index] = connection_gene.weight  
           
        # generate keras model             
        self.model = NeuralNet(architecture=architecture, 
                               input_size=self.input_size, 
                               output_size=self.output_size,
                               activation=self.activation,
                               optimizer=self.optimizer
                               )
        
        # set the weights with the arrays generated above
        self.model.set_weights(weights, biases)    
        
        self.architecture = architecture   
    
        return self.model
    

###############################################################################





# # example:
# input1 = NodeGene(bias=0, num=1, layer=0)
# input2 = NodeGene(bias=0, num=2, layer=0)
# input3 = NodeGene(bias=0, num=3, layer=0)
# input4 = NodeGene(bias=0, num=4, layer=0)
# hidden5 = NodeGene(bias=0, num=5, layer=0.5)
# output6 = NodeGene(bias=0, num=6, layer=1)
# output7 = NodeGene(bias=0, num=7, layer=1)

# con1 = input1.add_connection(hidden5, weight=0.1)
# con2 = input2.add_connection(hidden5, weight=0.2)
# con3 = input3.add_connection(hidden5, weight=0.3)
# con4 = input4.add_connection(output7, weight=0.4)
# con5 = hidden5.add_connection(output7, weight=0.5)

# activation=hidden_layer_activations[random.randint(0,len(hidden_layer_activations)-1)]
# optimizer=model_optimizers[random.randint(0,len(model_optimizers)-1)]

# chromosome = Chromosome(connection_genes=[con1, con2, con3, con4, con5],
#                         node_genes=[input1, input2, input3, input4,
#                                     hidden5,
#                                     output6, output7],
#                         activation=activation,
#                         optimizer=optimizer
#                         )

# NN = chromosome.compile_network()
# NN.get_weights(_print=True) 
