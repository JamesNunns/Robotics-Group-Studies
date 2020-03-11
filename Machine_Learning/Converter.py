import pickle
from neat import nn

with open("winner.pkl", "rb") as f:
    winner = pickle.load(f)

winner_net = nn.create_feed_forward_phenotype(winner)