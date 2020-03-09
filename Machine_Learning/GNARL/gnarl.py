# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:44:27 2020

@author: User
"""

import construct_net as net
import numpy as np
import gym


gym.logger.set_level(40)
env = gym.make('CartPole-v1')
env.reset()



hidden_layer_activations = ['tanh', 'relu', 'sigmoid', 'linear', 'softmax']
model_optimizers = ['adam', 'rmsprop']
max_fitness = 1


class Gnarl():
    def __init__(self,
                 input_size=2,
                 output_size=4,
                 max_generations=20, # implement
                 population_size=50, # implement
                 bias=None,   ## nEed to implement bias input node
                 mean_init_nodes=5,
                 mean_init_links=4,
                 alpha=1,
                 max_node_mods=3,
                 max_link_mods=5,
                 min_mods=0,
                 chromosome=None):
        

            
        self.input_size = input_size
        self.output_size = output_size
        self.max_node_mods = max_node_mods
        self.max_link_mods = max_link_mods
        self.min_mods = min_mods
        self.max_fitness = 200 ## random # pretty much
        self.bias = [4, 3] # used to bias the connections between outer nodes
        self.alpha = alpha

        self.init_nodes = np.random.randint(1, 2*mean_init_nodes)
        self.max_links = input_size * self.init_nodes + self.init_nodes * output_size
        self.init_links = np.random.randint(0, 2*mean_init_links)
        self.init_weights = np.random.uniform(low=-1.0, high=1.0, size=self.init_links)
        self.links = 0
        self.nodes = self.init_nodes + self.input_size + self.output_size
        
        if chromosome is None:
            self.initial_structure()
        
        

    def initial_structure(self):
        '''
        Creates the inital net currently given a fixed input and output size
        the # of hidden nodes is random and all links are random with a 2*bias
        towards a connection being to/from a input/output node
        '''
        input1 = net.NodeGene(bias=0, num=1, layer=0)
        input2 = net.NodeGene(bias=0, num=2, layer=0)
        input3 = net.NodeGene(bias=0, num=3, layer=0)
        input4 = net.NodeGene(bias=0, num=4, layer=0)
        output5 = net.NodeGene(bias=0, num=5, layer=1)
        output6 = net.NodeGene(bias=0, num=6, layer=1)
        # 4 in

        starting_nodes = self.input_size + self.output_size
        # array for the total # of in and out nodes, used for giving the other new hidden nodes #s

        hidden_nodes = []

        for i in range(1, self.init_nodes):
            hidden_nodes.append(net.NodeGene(bias=0, num=i+starting_nodes,
                                             layer=np.random.random()))

        self.chromosome = net.Chromosome(node_genes=[
            input1, input2, input3, input4,
            output5, output6]+hidden_nodes)


        all_nodes = self.get_biased_node()
        
        i = 0

        while self.links != self.init_links:
            link = np.random.choice(all_nodes, size=2)
            new_con = link[0].add_connection(link[1], weight=self.init_weights[i])
            if new_con is not None:
                # print(new_con,'adasd')
                self.chromosome.connection_genes.append(new_con)
                self.links += 1
                i += 1

    def get_reduced_temp(self):
        '''
        reduced temperature used in calculations to determine mutations
        '''
        return np.random.random() * (1 - 100/self.max_fitness)

    def number_of_mutations(self, max_mods):
        '''
        choses the number of structural mutations to be made
        '''
        total_mods = self.min_mods + (np.random.random() *
                                      self.get_reduced_temp() *
                                      (max_mods - self.min_mods))
        return round(total_mods)

    def mutate_link(self, link):
        '''
        mutates an individual link weight
        '''
        new_weight = link.weight + np.random.normal(0, self.alpha*
                                                    self.get_reduced_temp())
        link.weight = new_weight

    def mutate_weights(self):
        '''
        mutates the weight of all links
        '''
        for link in self.chromosome.connection_genes:
            self.mutate_link(link)

    def mutate_structure_node_add(self):
        '''
        '''
        new_nodes = self.number_of_mutations(self.max_node_mods)
        for i in range(new_nodes):
            new_node = net.NodeGene(bias=0, num=i+self.nodes,
                                    layer=np.random.random())
            self.chromosome.node_genes.append(new_node)
            self.nodes += 1

    def mutate_structure_node_del(self):
        ''' delete some random nodes'''
        del_nodes = self.number_of_mutations(self.max_node_mods)

        if self.input_size + self.output_size < len(self.chromosome.node_genes):
            for i in range(del_nodes):
            # ''' choose a random node that has a layer not equal to 1 or  0'''

                del self.chromosome.node_genes[np.random.randint(
                    self.input_size+self.output_size,
                    len(self.chromosome.node_genes))]
                self.nodes -= 1

    def mutate_structure_link_add(self):
        '''
        do this
        '''

        new_links = self.number_of_mutations(self.max_link_mods)
        # print('adding {0} new links'.format(new_links))
        links_made = 0
        while links_made != new_links:

            vector = [np.random.choice(self.get_biased_node()),
                      np.random.choice(self.get_biased_node())]
            new_con = vector[0].add_connection(vector[1], weight=0)
            
            if new_con is not None:
                self.chromosome.connection_genes.append(new_con)
                links_made += 1
                self.links += 1

    def mutate_structure_link_del(self):
        '''
        deletes a random node 
        '''
        del_links = self.number_of_mutations(self.max_link_mods)
        for i in range(del_links):
            del_link = np.random.choice(self.get_biased_link())
            del self.chromosome.connection_genes[self.chromosome.connection_genes.index(del_link)]
            self.links -= 1

    def get_biased_node(self, bias=[2, 1]):
        '''
        bias = [a,b] there will be a*outer nodes and b*inner nodes
        '''
        outer_nodes = [x for x in self.chromosome.node_genes if x.layer == 0 or x.layer == 1]
        # Finds the node objects on the outside
        inner_nodes = [x for x in self.chromosome.node_genes if x.layer != 0 and x.layer != 1]
        return self.bias[0]*outer_nodes + self.bias[1]*inner_nodes


    def get_biased_link(self):
        '''
            
        '''
        outer_links = []
        inner_links = []
        for link in self.chromosome.connection_genes:
            if link.vector[0].layer == 0:
                outer_links.append(link)

            elif link.vector[1].layer == 1:
                outer_links.append(link)

            else:
                inner_links.append(link)

        return self.bias[0]*outer_links + self.bias[1]*inner_links


    def mutate(self):
        self.mutate_weights()
        # try:
        #     self.mutate_structure_link_del() # MAYbe
        # except:
        #     pass
        self.mutate_structure_link_add() # WORKING
        # self.mutate_structure_node_del() # WORKING
        # self.mutate_structure_node_add() # WORKING?

    def run(self):
        
        model = self.chromosome
        for gen in range(self.max_generations):
            for pop in range(self.population_size):
                fitness = play_cart(model)
                
    def copy(self):
        return self.__class__(*self)
                
                
                

#my_net = Gnarl()
# my_net.initial_structure()


# print(my_net.chromosome.connection_genes)
#for conn in my_net.chromosome.connection_genes:
#    print(conn.weight)

#for i in range(100):
#    my_net.mutate()
#print('\n--Mutating--\n')

# for conn in my_net.chromosome.connection_genes:
#     print(conn.weight)

    # print(node.get_connections)
# my_net.mutate()

# for node in my_net.chromosome.node_genes:
#     node.get_connections()

# my_net.mutate()

#for node in my_net.chromosome.node_genes:
#    node.get_connections()




def play_cart(model, goal_steps=500, render=False, games=1, _print=True): 
    score = 0
    prev_obs = []
    done = False
    while not done:
        
        if len(prev_obs) == 0:
            action = np.random.randint(0,2)
        else:
            action = np.argmax(model.predict(prev_obs))
            
        observation, reward, done, info = env.step(action)
        prev_obs = observation
        score += reward
    
    env.reset()
    return score

'''
Currently being passed in a constant value of fitness 100 (out of max 200)
need to implement a method that gets the fitness at each stage in the sim and
makes changes accordingly
pass fitness to temp func
may need to change the structurl node mutation to not delete input or output nodes
Something is not right
The input nodes seem to like to connect to things they are already connected too

'''

'''

GenerATE A population of 100 or so each being unique nets generated given
the constaints passed into gnarl class

run the sim for each and get a measure of their fitness,

discard the worst 50%

copy the bst 50% and mutate the copies


'''
    
