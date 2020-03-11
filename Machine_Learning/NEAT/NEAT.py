import argparse
import os
import numpy as np
from neat import nn, population, statistics, parallel

parser = argparse.ArgumentParser(description='OpenAI Gym Solver')
parser.add_argument('--max-steps', dest='max_steps', type=int, default=1000, help='The max number of steps to take per genome (timeout)')
parser.add_argument('--episodes', type=int, default=1, help="The number of times to run a single genome. This takes the fitness score from the worst run")
parser.add_argument('--render', action='store_true')
parser.add_argument('--generations', type=int, default=50, help="The number of generations to evolve the network")
parser.add_argument('--checkpoint', type=str, help="Uses a checkpoint to start the simulation")
parser.add_argument('--num-cores', dest="numCores", type=int, default=6, help="The number cores on your computer for parallel execution")
args = parser.parse_args()

class NEAT:
    '''
    NEAT using the neat-python module.
    '''
    
    def __init__(self, env, config, threads: int = 4):
        print("\n------------------------------------------")
        print("               NEAT USING THE               ")
        print("            NEAT-PYTHON LIBRARY             ")
        print("------------------------------------------\n")

        self.env = env

        # Simulation
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, config)
        pop = population.Population(config_path) # Get the config file

        # Load checkpoint
        if args.checkpoint:
            pop.load_checkpoint(args.checkpoint)
        
        # Start simulation
        try:
            if threads == 1:
                pop.run(self.eval_fitness, args.generations)
            else:
                pe = parallel.ParallelEvaluator(threads, self.evaluate_genome)
                pop.run(pe.evaluate, args.generations)
        except KeyboardInterrupt:
            print("\nExited.")

        pop.save_checkpoint("checkpoint") # Save the current checkpoint

        # Log statistics.
        statistics.save_stats(pop.statistics)
        statistics.save_species_count(pop.statistics)
        statistics.save_species_fitness(pop.statistics)

        print('Number of evaluations: {0}'.format(pop.total_evaluations))

        # Show output of the most fit genome against training data.
        winner = pop.statistics.best_genome()

        # Save best network
        name = input("Net name: ")
        import pickle
        with open(name + '.pkl', 'wb') as output:
            pickle.dump(winner, output, 1)
        print("Net saved as " + name + '.pkl')

        print('\nBest genome:\n{!s}'.format(winner))
        input("Press enter to run the best genome...")

        winner_net = nn.create_feed_forward_phenotype(winner)
        self.simulate_species(winner_net, env, 1, args.max_steps, render=True)

    def simulate_species(self, net, env, episodes=1, steps=50000, render=False):
        '''
        Run simulations for one species with a given net.
        '''
        if render: env.render(net)
        fitnesses = []
        for runs in range(episodes):
            inputs = env.reset()
            cum_reward = 0.0
            for j in range(steps):
                outputs = net.serial_activate(inputs)
                action = np.argmax(outputs)
                inputs, reward, done, _ = env.step(action)
                if done:
                    break
                cum_reward += reward

            fitnesses.append(cum_reward)

        fitness = np.array(fitnesses).mean()
        # print("Fitness: %s" % str(fitness))
        return fitness

    def evaluate_genome(self, g):
        '''
        Worker for multithreading.
        '''
        net = nn.create_feed_forward_phenotype(g)
        return self.simulate_species(net, self.env, args.episodes, args.max_steps, render=args.render)

    def eval_fitness(self, genomes):
        '''
        Evaluate fitness of genomes.
        '''
        for g in genomes:
            fitness = self.evaluate_genome(g)
            g.fitness = fitness



# MAIN

def main():
    print("\nPlease select environment:")
    print(" [1] OpenAI Gym CartPole-v0")
    print(" [2] Pymunk")
    print(" [3] 3D Unity")

    environment = input("--> ")

    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    if environment == '1': # Run Gym sim
        print("Running NEAT with the OpenAI Gym CartPole-v0 environment...\n")
        import gym
        NEAT(gym.make('CartPole-v0'), 'gym_config', threads=4)
    elif environment == '2': # Run Pymunk sim
        print("Running NEAT with the Pymunk environment...\n")
        from Pymunk import Swing
        NEAT(Swing(), 'pymunk_config', threads=4)
    elif environment == '3': # Run Unity sim
        print("Running NEAT with the 3D Unity environment...\n")
        from Unity import Unity
        NEAT(Unity(), 'pymunk_config', threads=1)


if __name__ == "__main__":
    main()
    # train_network(env, 'pymunk_config')