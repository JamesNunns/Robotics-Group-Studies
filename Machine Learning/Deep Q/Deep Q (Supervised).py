import gym
import random
import numpy as np
from keras.models     import Sequential
from keras.layers     import Dense
from keras.optimizers import Adam
from Environment import Swing
from tqdm import tqdm
import matplotlib.pyplot as plt

env = Swing()
env.reset()
goal_steps = 3600
score_requirement = 60
intial_games = 10000

print("\n------------------------------------------")
print("          DEEP Q-LEARNING USING             ")
print("                NEURAL NETS                 ")
print("------------------------------------------\n")

def model_data_preparation():
    print("Obtaining training data...")

    training_data = []
    accepted_scores = []
    for game_index in tqdm(range(intial_games)):
        score = 0
        game_memory = []
        previous_observation = []
        for step_index in range(goal_steps):
            action = random.randrange(0, 4)
            observation, reward, done = env.step(action)
            
            if len(previous_observation) > 0:
                game_memory.append([previous_observation, action])
                
            previous_observation = observation
            score += reward
            if done:
                break
            
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                if data[1] == 0:
                    output = [1, 0, 0, 0, 0]
                elif data[1] == 1:
                    output = [0, 1, 0, 0, 0]
                elif data[1] == 2:
                    output = [0, 0, 1, 0, 0]
                elif data[1] == 3:
                    output = [0, 0, 0, 1, 0]
                elif data[1] == 4:
                    output = [0, 0, 0, 0, 1]
                training_data.append([data[0], output])
        
        env.reset()
    
    print("Done!\n")
    return training_data

def build_model(input_size, output_size):
    print(" |")
    print(" +--> Building model...")

    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation='relu'))
    model.add(Dense(52, activation='relu'))
    model.add(Dense(output_size, activation='linear'))
    model.compile(loss='mse', optimizer=Adam())

    print(" +--> Done!")
    return model

def train_model(training_data):
    print("Training model...")

    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))

    print(" |")
    print(" +--> Fitting model...")
    model.fit(X, y, epochs=3)
    print(" +--> Done!")

    print(" V")
    print("Done!\n")
    return model

def graph(trained_model):
    print("Plotting graph...")

    done = False
    prev_obs = []
    angles = []
    while not done:
        if len(prev_obs) == 0:
            action = random.randrange(0,4)
        else:
            action = np.argmax(trained_model.predict(prev_obs.reshape(-1, len(prev_obs)))[0])

        new_observation, reward, done = env.step(action)
        prev_obs = np.array(new_observation)
        angles.append(env.rod1._get_angle())
    plt.plot(np.linspace(0, 60, 60*60+1), angles)
    plt.show()

    print("Done!")


training_data = model_data_preparation()
trained_model = train_model(training_data)
graph(trained_model)
env.render(trained_model)

# scores = []
# choices = []
# for each_game in range(100):
#     score = 0
#     prev_obs = []
#     for step_index in range(goal_steps):
#         env.render()
#         if len(prev_obs)==0:
#             action = random.randrange(0,4)
#         else:
#             action = np.argmax(trained_model.predict(prev_obs.reshape(-1, len(prev_obs)))[0])
        
#         choices.append(action)
#         new_observation, reward, done = env.step(action)
#         prev_obs = new_observation
#         score+=reward
#         if done:
#             break

#     env.reset()
#     scores.append(score)

# print(scores)
# print('Average Score:', sum(scores)/len(scores))
# print('choice 1:{}  choice 0:{}'.format(choices.count(1)/len(choices),choices.count(0)/len(choices)))