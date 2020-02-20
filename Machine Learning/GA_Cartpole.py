"""
This file contains a variation os my resolution for the Open.Ai CartPole-V1 challenge, but now using a Genetic Algorithm
Enjoy and Learn
Th3 0bservator
December, 01, 2019
"""


import os
import random
import gym
import pandas as pd
import numpy as np
# import tensorflow as tf
import time
from keras.models import Sequential
from keras.layers import Dense, Dropout, InputLayer
from keras import backend as K

# Define Game Commands
RIGHT_CMD = [0, 1]
LEFT_CMD = [1, 0]

# Define Reward Config
START_REWARD = 0
MIN_REWARD = 250

# Define Hyperparameters for NN
HIDDEN_LAYER_COUNT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
HIDDEN_LAYER_NEURONS = [8, 16, 24, 32, 64, 128, 256, 512]
HIDDEN_LAYER_RATE = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
HIDDEN_LAYER_ACTIVATIONS = ['tanh', 'relu', 'sigmoid', 'linear', 'softmax']
HIDDEN_LAYER_TYPE = ['dense', 'dropout']
MODEL_OPTIMIZER = ['adam', 'rmsprop']

# Define Genetic Algorithm Parameters
MAX_GENERATIONS = 50  # Max Number of Generations to Apply the Genetic Algorithm
POPULATION_SIZE = 20  # Max Number of Individuals in Each Population
BEST_CANDIDATES_COUNT = 4  # Number of Best Candidates to Use
RANDOM_CANDIDATES_COUNT = 2  # Number of Random Candidates (From Entire Population of Generation) to Next Population
OPTIMIZER_MUTATION_PROBABILITY = 0.1  # 10% of Probability to Apply Mutation on Optimizer Parameter
HIDDEN_LAYER_MUTATION_PROBABILITY = 0.1  # 10% of Probability to Apply Mutation on Hidden Layer Quantity

# Initialize Game Environment
env = gym.make('CartPole-v1')


class LayerLayout:

    """
    Define a Single Layer Layout
    """
    def __init__(self, layer_type):
        self.neurons = None
        self.activation = None
        self.rate = None
        self.layer_type = layer_type


class Chromosome:
    """
    Chromosome Class
    """

    def __init__(self, layer_layout, optimizer, specie):
        self.layer_layout = layer_layout
        self.optimizer = optimizer
        self.result_worst = None
        self.result_best = None
        self.result_avg = None
        self.result_sum = None
        self.specie = specie
        self.ml_model = None

    def safe_get_hidden_layer_node(self, index=0):
        """
        Return a Hidden Layer Node if Exists, Otherwise, returns None
        :param index:
        :return:
        """

        if len(self.layer_layout) > index:
            return self.layer_layout[index]

        return None


def play_random_games(games=100):
    """
    Play Random Games to Get Some Observations
    :param games:
    :return:
    """

    print("[+] Playing Random Games: ", end='', flush=True)
    run_start = time.time()

    # Storage for All Games Movements
    all_movements = []

    for episode in range(games):

        # Reset Game Reward
        episode_reward = 0

        # Define Storage for Current Game Data
        current_game_data = []

        # Reset Game Environment
        env.reset()

        # Get First Random Movement
        action = env.action_space.sample()

        while True:

            # Play
            observation, reward, done, info = env.step(action)

            # Get Random Action (On Real, its get a "Next" movement to compensate Previous Movement)
            action = env.action_space.sample()

            # Store Observation Data and Action Taken
            current_game_data.append(
                np.hstack((observation, LEFT_CMD if action == 0 else RIGHT_CMD))
            )

            if done:
                break

            # Compute Reward
            episode_reward += reward

        # Save All Data (Only for the Best Games)
        if episode_reward >= MIN_REWARD:
            all_movements.extend(current_game_data)

    # Create DataFrame
    df = pd.DataFrame(
        all_movements,
        columns=['cart_position', 'cart_velocity', 'pole_angle', 'pole_velocity_at_tip', 'action_to_left', 'action_to_right']
    )

    # Convert Action Columns to Integer
    df['action_to_left'] = df['action_to_left'].astype(int)
    df['action_to_right'] = df['action_to_right'].astype(int)

    run_stop = time.time()
    print(f"Done > Takes {run_stop - run_start} sec")

    return df


def generate_model_from_chromosome(df, chromosome):
    """
    Generate and Train Model using Chromosome Spec
    :param dataframe:
    :param chromosome:
    :return:
    """

    # Define Neural Network Topology
    m_model = Sequential()

    # Define Input Layer
    m_model.add(InputLayer(input_shape=(4,)))

    # Add Hidden Layers
    for layer in chromosome.layer_layout:

        if layer.layer_type == 'dense':
            m_model.add(
                Dense(
                    layer.neurons,
                    activation=layer.activation
                )
            )
        elif layer.layer_type == 'dropout':
            m_model.add(
                Dropout(rate=layer.rate)
            )

    # Define Output Layer
    m_model.add(Dense(2, activation='sigmoid'))

    # Compile Neural Network
    m_model.compile(optimizer=chromosome.optimizer, loss='categorical_crossentropy')

    # Fit Model with Data
    m_model.fit(
        df[['cart_position', 'cart_velocity', 'pole_angle', 'pole_velocity_at_tip']],
        df[['action_to_left', 'action_to_right']],
        epochs=20,
        verbose=0
    )

    # Update Model into Chromosome
    chromosome.ml_model = m_model


def create_random_layer():
    """
    Creates a new Randomly Generated Layer
    :return:
    """

    layer_layout = LayerLayout(
        layer_type=HIDDEN_LAYER_TYPE[random.randint(0, len(HIDDEN_LAYER_TYPE) - 1)]
    )

    if layer_layout.layer_type == 'dense':
        layer_layout.neurons = HIDDEN_LAYER_NEURONS[random.randint(0, len(HIDDEN_LAYER_NEURONS) - 1)]
        layer_layout.activation = HIDDEN_LAYER_ACTIVATIONS[random.randint(0, len(HIDDEN_LAYER_ACTIVATIONS) - 1)]

    elif layer_layout.layer_type == 'dropout':
        layer_layout.rate = HIDDEN_LAYER_RATE[random.randint(0, len(HIDDEN_LAYER_RATE) - 1)]

    return layer_layout


def generate_first_population_randomly(population_size=10):
    """
    Creates an Initial Random Population
    :param population_size:
    :return:
    """

    print("[+] Creating Initial NN Model Population Randomly: ", end='')

    result = []
    run_start = time.time()

    for current in range(population_size):

        # Choose Hidden Layer Count
        hidden_layer_count = HIDDEN_LAYER_COUNT[random.randint(0, len(HIDDEN_LAYER_COUNT)-1)]
        hidden_layer_layout = []

        # Define Layer Structure
        for current_layer in range(hidden_layer_count):
            hidden_layer_layout.append(create_random_layer())

        chromosome = Chromosome(
            layer_layout=hidden_layer_layout,
            optimizer=MODEL_OPTIMIZER[random.randint(0, len(MODEL_OPTIMIZER)-1)],
            specie=f"I {current}"
        )

        result.append(chromosome)

    run_stop = time.time()
    print(f"Done > Takes {run_stop-run_start} sec")

    return result


def generate_children(mother: Chromosome, father: Chromosome) -> Chromosome:
    """
    Generate a New Children based Mother and Father Genomes
    :param mother: Mother Chromosome
    :param father: Father Chromosome
    :return: A new Children
    """

    # Layer Layout
    c_layer_layout = []
    layers_counts = len(mother.layer_layout) if random.randint(0, 1) == 0 else len(father.layer_layout)
    for ix in range(layers_counts):
        c_layer_layout.append(
            mother.safe_get_hidden_layer_node(ix) if random.randint(0, 1) == 0 else father.safe_get_hidden_layer_node(ix)
        )

    # Remove all Nones on Layers Layout
    c_layer_layout = [item for item in c_layer_layout if item is not None]

    # Optimizer
    c_optimizer = mother.optimizer if random.randint(0, 1) == 0 else father.optimizer

    chromosome = Chromosome(
        layer_layout=c_layer_layout,
        optimizer=c_optimizer,
        specie=""
    )

    return chromosome


def generate_reference_ml(df):
    """
    Train and Generate NN Model
    :param df: Dataframe to Training Process
    :return:
    """
    print("[+] Training Original NN Model: ", end='')
    run_start = time.time()

    # Define Neural Network Topology
    m_model = Sequential()
    m_model.add(Dense(64, input_dim=4, activation='relu'))
    m_model.add(Dense(64,  activation='relu'))
    m_model.add(Dense(32,  activation='relu'))
    m_model.add(Dense(2,  activation='sigmoid'))

    # Compile Neural Network
    m_model.compile(optimizer='adam', loss='categorical_crossentropy')

    # Fit Model with Data
    m_model.fit(
        df[['cart_position', 'cart_velocity', 'pole_angle', 'pole_velocity_at_tip']],
        df[['action_to_left', 'action_to_right']],
        epochs=20,
        verbose=0
    )

    run_stop = time.time()
    print(f"Done > Takes {run_stop-run_start} sec")

    return m_model


def mutate_chromosome(chromosome):
    """
    Apply Random Mutations on Chromosome
    :param chromosome: input Chromosome
    :return: Result Chromosome. May or May Not Contains a Mutation
    """

    # Apply Mutation on Optimizer
    if random.random() <= OPTIMIZER_MUTATION_PROBABILITY:
        chromosome.optimizer = MODEL_OPTIMIZER[random.randint(0, len(MODEL_OPTIMIZER)-1)]

    # Apply Mutation on Hidden Layer Size
    if random.random() <= HIDDEN_LAYER_MUTATION_PROBABILITY:

        new_hl_size = HIDDEN_LAYER_COUNT[random.randint(0, len(HIDDEN_LAYER_COUNT)-1)]

        # Check if Need to Expand or Reduce Layer Count
        if new_hl_size > len(chromosome.layer_layout):

            # Increase Layer Count
            while len(chromosome.layer_layout) < new_hl_size:
                chromosome.layer_layout.append(
                    create_random_layer()
                )

        elif new_hl_size < len(chromosome.layer_layout):

            # Reduce Layers Count
            chromosome.layer_layout = chromosome.layer_layout[0: new_hl_size]

        else:
            pass  # Do not Change Layer Size

    return chromosome


def play_game(ml_model, games=100, model_name="Reference Model"):
    """
    Play te Game
    :param ml_model:
    :param games:
    :return:
    """

    all_rewards = []

    for i_episode in range(games):

        # Define Reward Var
        episode_reward = 0

        # Reset Env for the Game
        observation = env.reset()

        while True:
            # env.render()  << Uncomment to allow the Open.AI Engine do Render the Game

            # Predict Next Movement
            current_action_pred = ml_model.predict(observation.reshape(1, 4))

            # Define Movement
            current_action = np.argmax(current_action_pred)

            # Make Movement
            observation, reward, done, info = env.step(current_action)

            if done:
                episode_reward += 1
                break

            episode_reward += 1

        all_rewards.append(episode_reward)

    # Return Worst, Avg, Best and Sum of Rewards
    r_worst = np.min(all_rewards)
    r_best = np.max(all_rewards)
    r_avg = np.average(all_rewards)
    r_sum = np.sum(all_rewards)

    return r_worst, r_best, r_avg, r_sum


def evolve_population(population):
    """
    Evolve and Create the Next Generation of Individuals
    :param population: Current Population
    :return: A new population
    """

    # Clear Graphs from Keras e TensorFlow
    K.clear_session()
    keras.reset_default_graph()

    # Select N Best Candidates + Y Random Candidates. Kill the Rest of Chromosomes
    parents = []
    parents.extend(population[0:BEST_CANDIDATES_COUNT])  # N Best Candidates
    for rn in range(RANDOM_CANDIDATES_COUNT):
        parents.append(population[random.randint(0, POPULATION_SIZE - 1)])  # Y Random Candidate

    # Create New Population Through Crossover
    new_population = []
    new_population.extend(parents)

    # Fill Population with new Random Children with Mutation
    while len(new_population) < POPULATION_SIZE:
        parent_a = random.randint(0, len(parents) - 1)
        parent_b = random.randint(0, len(parents) - 1)
        while parent_a == parent_b:
            parent_b = random.randint(0, len(parents) - 1)

        new_population.append(
            mutate_chromosome(
                generate_children(
                    mother=parents[parent_a],
                    father=parents[parent_b]
                )
            )
        )

    return new_population


def main():

    # Play Random (Initial) Games to create Test and Training Data
    df = play_random_games(games=10000)

    print("\n********** Reference Network Model **********")

    # Creates a Reference NN Model bases on CartPole.py Sample
    ml_model = generate_reference_ml(df)

    # Play Games with Reference NN Model
    print("[+] Playing Games with Reference NN Model \t>", end='', flush=True)
    ref_worst, ref_best, ref_avg, ref_sum = play_game(ml_model=ml_model, games=100)
    print(f"\tWorst Score:{ref_worst} | Average Score:{ref_avg} | Best Score:{ref_best} | Total Score:{ref_sum}")

    # >>>>>> Genetic Algorithm Section <<<<<<
    print("\n********** Genetic Algorithm **********")
    population = generate_first_population_randomly(
        population_size=POPULATION_SIZE
    )

    # Run Each Generation
    for current_generation in range(MAX_GENERATIONS):
        print(f"[+] Generation {current_generation+1} of {MAX_GENERATIONS}")
        i = 0

        # >>>>>> Training Phase <<<<<<
        print(f"\tTraining Models: ", end='', flush=True)
        training_start = time.time()

        # Train all Models in Population
        for individual in population:
            generate_model_from_chromosome(df, individual)

        training_stop = time.time()
        print(f"Done > Takes {training_stop - training_start} sec")

        # >>>>>> Evaluation Phase <<<<<<
        print(f"\tEvaluating Population: ", end='', flush=True)
        evaluation_start = time.time()

        for individual in population:

            # Play the Games
            score_worst, score_best, score_avg, score_sum = play_game(
                ml_model=individual.ml_model,
                games=100,
                model_name=individual.specie
            )

            # Update Chromosome Results
            individual.result_worst = score_worst
            individual.result_best = score_best
            individual.result_avg = score_avg
            individual.result_sum = score_sum

            # Update Indexer
            i += 1

        evaluation_stop = time.time()
        print(f"Done > Takes {evaluation_stop - evaluation_start} sec")

        # Sort Candidates by Sum of Results
        population.sort(key=lambda x: x.result_sum, reverse=True)

        # Compute Generation Metrics
        gen_score_avg = np.average([item.result_avg for item in population])
        gen_score_min = np.min([item.result_worst for item in population])
        gen_score_max = np.max([item.result_best for item in population])
        gen_score_sum = np.sum([item.result_sum for item in population])

        print(f"\tWorst Score:{gen_score_min} | Average Score:{gen_score_avg} | Best Score:{gen_score_max} | Total Score:{gen_score_sum}")

        # >>>>>> Genetic Selection, Children Creation and Mutation <<<<<<
        population = evolve_population(population)


if __name__ == "__main__":

    # Disable Tensorflow Warning Messages
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # Run Program
    main()