using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Interfaces;
using Keras;

// input_size = 2
// output_size = 2

namespace Interfaces.Algorithms {
    class Agent : IEntity {
        var neural_net;
        int epsilon;
        int epsilon_decay;
        int epsilon_min;
        float[][] prev_states;
        int action;

        public Agent(var neural_net) {
            neural_net = neural_net;
            List<List<var>> memory = new List<List<int>>();
            List<int> performance = new List<int>();

            epsilon = 1;
            epsilon_decay = 0.995;
            epsilon_min = 0.01;

            prev_states = new float[2][2];
            prev_state[0][0] = 0
            prev_state[0][1] = 0
            action = 0;
        }

        public int[] perform_action(float[] state, float reward, bool done) {
            prev_states[0] = prev_states[1];
            prev_states[1] = state;

            memory.Add(new List<var>{prev_states[0], action, reward, prev_state[1], done})
            performance.Add(reward)

            epsilon = Math.Max(epsilon_min, Math.Min(epsilon, 1.0 - Math.Log10(memory.Count * epsilon_decay / 10000)));
            Random random = new Random();
            if (random.NextDouble() <= epsilon) {
                action = random.Next(0, 5)
            } else {
                prediction = neural_net.predict(state[1]);
                int maxValue = prediction.Max();
                int maxIndex = prediction.ToList().IndexOf(maxValue);
                action = maxIndex;
            }

            int[] output = new int[2]{0, 0};
            if (action == 0) {
                output[0] = 1;
            } else if (action == 1) {
                output[0] = -1;
            } else if (action == 2) {
                output[1] = 1;
            } else if (action == 3) {
                output[1] = -1;
            }

            return output;
        }
    }

    class Controller : IGenerationController {
        float alpha;
        float alpha_decay;
        float gamma;
        List<Agent> agents = new List<Agent>();

        public Controller() {
            alpha = 0.01;
            alpha_decay = 0.01;
            gamma = 1.0;
        }

        public void make_agent() {
            var neural_net = new Sequential();
            neural_net.Add(new Dense(52, activation: 'tanh', input_shape: new Shape(2)));
            neural_net.Add(new Dense(128, activation: 'tanh'));
            neural_net.Add(new Dense(2, activation: 'linear'));
            neural_net.Compile(loss: 'mse', optimizer: new Adam(lr: alpha, decay: alpha_decay));

            agents.Add(new Agent(neural_net));
        }

        public void replay(Agent agent, int batch_size: 64) {
            List<int> x_batch = new List<int>();
            List<int> y_batch = new List<int>();

            Random random = new Random();
            List<int> mini_batch = agent.memory.OrderBy(x => rnd.Next()).Take(Math.Min(agent.memory.Count, batch_size));

            for ((state, action, reward, next_state, done) in mini_batch) {
                int y_target = agent.neural_net.predict(state);
                if (done) {
                    y_target[0][action] = reward;
                } else {
                    y_target[0][action] = reward + gamma * Math.Max(agent.neural_net.predict(next_state)[0]);
                }
                x_batch.Add(state[0]);
                y_batch.Add(y_target[0]);
            }
            
            agent.neural_net.Fit(x_batch, y_batch, batch_size: x_batch.Count, verbose: 0);
        }

        public Controller step() {
            for (agent in agents) {
                this.replay(agent);
            }

            return this;
        }
    }
