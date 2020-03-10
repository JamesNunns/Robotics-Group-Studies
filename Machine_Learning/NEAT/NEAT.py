import argparse
import os
import numpy as np
from neat import nn, population, statistics, parallel

parser = argparse.ArgumentParser(description='OpenAI Gym Solver')
parser.add_argument('--max-steps', dest='max_steps', type=int, default=1000,
                    help='The max number of steps to take per genome (timeout)')
parser.add_argument('--episodes', type=int, default=1,
                    help="The number of times to run a single genome. This takes the fitness score from the worst run")
parser.add_argument('--render', action='store_true')
parser.add_argument('--generations', type=int, default=50,
                    help="The number of generations to evolve the network")
parser.add_argument('--checkpoint', type=str,
                    help="Uses a checkpoint to start the simulation")
parser.add_argument('--num-cores', dest="numCores", type=int, default=4,
                    help="The number cores on your computer for parallel execution")
args = parser.parse_args()


def simulate_species(net, env, episodes=1, steps=50000, render=False):
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
    print("Species fitness: %s" % str(fitness))
    return fitness

class NEAT:

    def __init__(self, env, config):
        self.env = env

        # Simulation
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, config)
        pop = population.Population(config_path)
        # Load checkpoint
        if args.checkpoint:
            pop.load_checkpoint(args.checkpoint)
        # Start simulation
        if args.render:
            pop.run(self.eval_fitness, args.generations)
        else:
            pe = parallel.ParallelEvaluator(args.numCores, self.worker_evaluate_genome)
            pop.run(pe.evaluate, args.generations)

        pop.save_checkpoint("checkpoint")

        # Log statistics.
        statistics.save_stats(pop.statistics)
        statistics.save_species_count(pop.statistics)
        statistics.save_species_fitness(pop.statistics)

        print('Number of evaluations: {0}'.format(pop.total_evaluations))

        # Show output of the most fit genome against training data.
        winner = pop.statistics.best_genome()

        # Save best network
        import pickle
        with open('winner.pkl', 'wb') as output:
            pickle.dump(winner, output, 1)

        print('\nBest genome:\n{!s}'.format(winner))
        print('\nOutput:')

        input("Press Enter to run the best genome...")
        winner_net = nn.create_feed_forward_phenotype(winner)
        for i in range(100):
            simulate_species(winner_net, env, 1, args.max_steps, render=True)

    def worker_evaluate_genome(self, g):
        net = nn.create_feed_forward_phenotype(g)
        return simulate_species(net, self.env, args.episodes, args.max_steps, render=args.render)
        
    def evaluate_genome(self, g):
        net = nn.create_feed_forward_phenotype(g)
        return simulate_species(net, self.env, args.episodes, args.max_steps, render=args.render)

    def eval_fitness(self, genomes):
        for g in genomes:
            fitness = self.evaluate_genome(g)
            g.fitness = fitness

def main():
    environment = input("Environment (gym / pymunk / unity): ")

    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    if environment == 'gym': # Run Gym sim
        import gym
        NEAT(gym.make('CartPole-v0'), 'gym_config')
    elif environment == 'pymunk': # Run Pymunk sim
        from Pymunk import Swing
        NEAT(Swing(), 'pymunk_config')
    elif environment == 'unity': # Run Unity sim
        from Unity import Unity
        NEAT(Unity(), 'pymunk_config')


if __name__ == "__main__":
    main()
    # train_network(env, 'pymunk_config')