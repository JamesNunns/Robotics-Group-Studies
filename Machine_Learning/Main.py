#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    algorithm = input("Algorithm (deepq / simplee / neat / gnarl): ")

    if algorithm == 'deepq':
        sys.path.insert(1, 'DeepQ')
        import DeepQ
        DeepQ.main()
    elif algorithm == 'simplee':
        sys.path.insert(1, 'SimpleE')
        import SimpleE
        SimpleE.main()
    elif algorithm == 'neat':
        sys.path.insert(1, 'NEAT')
        import NEAT
        NEAT.main()
    elif algorithm == 'gnarl':
        sys.path.insert(1, 'GNARL')
        import GNARL
        GNARL.main()