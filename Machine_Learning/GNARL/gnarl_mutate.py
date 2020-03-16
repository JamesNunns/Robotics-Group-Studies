# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:44:27 2020

@author: Henry
"""


import numpy as np
import gym
import copy

import construct_net_gnarl as net

# gym.logger.set_level(40)
# env = gym.make('CartPole-v1')
# env.reset()



hidden_layer_activations = ['tanh', 'relu', 'sigmoid', 'linear', 'softmax']
model_optimizers = ['adam', 'rmsprop']
max_fitness = 1


class Gnarl():
    '''
    class used to generate and mutate a neural net using the GNARL algorithm
    '''
    def __init__(self,
                 env=None,
                 engine=None,
                 input_size=4,
                 output_size=2,
                 max_generations=20, # implement
                 population_size=50, # implement
                 bias=None,   ## nEed to implement bias input node
                 mean_init_nodes=12,
                 mean_init_links=40,
                 alpha=1,
                 max_node_mods=3,
                 max_link_mods=5,
                 min_mods=0,
                 chromosome=None,
                 fitness=None,
                 max_fitness=500):
        
     
        # if engine is None:
        self.env = env
        self.engine = engine
        self.env.reset()

        self.input_size = input_size
        self.output_size = output_size
        self.max_node_mods = max_node_mods
        self.max_link_mods = max_link_mods
        self.min_mods = min_mods
        self.max_fitness = max_fitness ## random # pretty much
        self.bias = [5, 4] # used to bias the connections between outer nodes 
        self.alpha = alpha
        self.max_generations = max_generations
        self.population_size = population_size

        self.init_nodes = np.random.randint(1, 2*mean_init_nodes)
        self.max_links = input_size * self.init_nodes + self.init_nodes * output_size
        self.init_links = np.random.randint(0, 2*mean_init_links)
        self.init_weights = np.random.uniform(low=-1.0, high=1.0, size=self.init_links)
        self.links = 0
        self.nodes = self.init_nodes + self.input_size + self.output_size

        if chromosome is None:
            self.initial_structure()

        if fitness is None:
            self.fitness = 4
        else:
            self.fitness = fitness





    def initial_structure(self):
        '''
        Creates the inital net currently given a fixed input and output size
        the # of hidden nodes is random and all links are random with a 2*bias
        towards a connection being to/from a input/output node
        '''
        input_nodes = []
        output_nodes = []
        for i in range(self.input_size):
            input_nodes.append(net.NodeGene(bias=0, num=1, layer=0))

        for i in range(self.output_size):
            output_nodes.append(net.NodeGene(bias=0, num=1, layer=1))

        starting_nodes = self.input_size + self.output_size
        # array for the total # of in and out nodes, used for giving the other new hidden nodes #s

        hidden_nodes = []

        for i in range(0, self.init_nodes):
            hidden_nodes.append(net.NodeGene(bias=0, num=i+starting_nodes,
                                             layer=np.random.random()))

        self.chromosome = net.Chromosome(node_genes=input_nodes + hidden_nodes + output_nodes)

        all_nodes = self.get_biased_node()

        i = 0
        
        
        '''
        Fix this
        '''
        max_links = self.get_max_links()
            
            
            
        # This is a bad fix
        while self.links < min([self.init_links, max_links]):
            # print('links: {}, init_links: {}, max_links: {}'.format(self.links, self.init_links, max_links))
            # print('aaa',len(self.chromosome.node_genes))
            # print(self.nodes,'\n')
            
            link = np.random.choice(all_nodes, size=2)
            new_con = link[0].add_connection(link[1], weight=self.init_weights[i])

            if new_con is not None:

                self.chromosome.connection_genes.append(new_con)
                self.links += 1
                i += 1

    def get_reduced_temp(self):
        '''
        reduced temperature used in calculations to determine mutations
        '''
        return np.random.random() * (1 - self.fitness/self.max_fitness)

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
        adds a node randomly
        '''
        new_nodes = self.number_of_mutations(self.max_node_mods)
        for i in range(new_nodes):
            new_node = net.NodeGene(bias=0, num=i+self.nodes,
                                    layer=np.random.random())
            self.chromosome.node_genes.append(new_node)
            self.nodes += 1

    def mutate_structure_node_del(self):
        ''' 
        delete some random nodes
        '''
        del_nodes = self.number_of_mutations(self.max_node_mods)

        if self.input_size + self.output_size <= len(self.chromosome.node_genes):
            for i in range(del_nodes):
            # ''' choose a random node that has a layer not equal to 1 or  0'''
                if self.input_size + self.output_size != len(self.chromosome.node_genes):
                    node_delete = self.chromosome.node_genes[np.random.randint(
                        self.input_size+self.output_size,
                        len(self.chromosome.node_genes))]

                    del node_delete


                '''
                get all the links from the chosen node
                remove from self.cromsone link_genese
                '''

                self.nodes -= 1

    def mutate_structure_link_add(self):
        '''
        do this
        '''

        new_links = self.number_of_mutations(self.max_link_mods)


        links_made = 0
        tries = 0

        while links_made != new_links and tries < 20:
            tries += 1

            vector = [np.random.choice(self.get_biased_node()),
                      np.random.choice(self.get_biased_node())]
            new_con = vector[0].add_connection(vector[1], weight=0)

            if new_con is not None:
                self.chromosome.connection_genes.append(new_con)
                links_made += 1
                self.links += 1


    def mutate_structure_link_del(self):
        '''
        deletes a random (biased) node
        '''

        del_links = self.number_of_mutations(self.max_link_mods)
        # Number of nodes to delete


        for i in range(del_links):
            bias_link = self.get_biased_link()
            del_link = np.random.choice(bias_link)
            del self.chromosome.connection_genes[self.chromosome.connection_genes.index(del_link)]
            net.delete_link(del_link)
            self.links -= 1



    def get_biased_node(self, bias=[2, 1]):
        '''
        bias = [a,b] there will be a*outer nodes and b*inner nodes
        '''
        outer_nodes = [x for x in self.chromosome.node_genes if x.layer == 0 or x.layer == 1]
        # Finds the node objects on the outside
        inner_nodes = [x for x in self.chromosome.node_genes if x.layer != 0 and x.layer != 1]
        # print(len(inner_nodes))
        return self.bias[0]*outer_nodes + self.bias[1]*inner_nodes


    def get_biased_link(self):
        '''
        Returns a list of all the outter and hidden links with bias[0] instances
        of every outer link and bias[1] instances of every hidden link

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
        '''
            Calls all the individual mutate functions
        '''        
        self.mutate_weights()

        try:
            self.mutate_structure_link_del()

        except:
            pass
        self.mutate_structure_link_add()

        self.mutate_structure_node_del()

        self.mutate_structure_node_add()



    def run(self):
        '''
        runs
        '''

        self.fitness = self.play_cart(self.chromosome)



    def ret(self):
        '''
        returns a deep copy of iteself to be used as the offspring
        '''
        return copy.deepcopy(self)
    
        
    def get_max_links(self):
        hidden_nodes = (self.nodes - self.input_size - self.output_size)
        links = self.input_size * (self.output_size + hidden_nodes) 
        for i in range(hidden_nodes+1, 1, -1):
            links += i
        return links


    def play_cart(self, chromosome, goal_steps=500):
        
        score = 0
        prev_obs = []
        done = False
        model = chromosome.compile_network()
        
        while not done:
    
            if len(prev_obs) == 0:
                action = np.random.randint(0, self.output_size)
                # print('bad')
            else:
                # print('good')
                action = np.argmax(model.predict(prev_obs))
                
            observation, reward, done, info = self.env.step(action)
            prev_obs = observation
            score += reward
    
        self.env.reset()
        return score


if __name__ == '__main__':

    my_net = Gnarl(env = gym.make('CartPole-v1'))

    for i in range(100):
        print(my_net.fitness)
        print('Generation: {}'.format(i))
        my_net.run()

    print('\n--Mutating--\n')


