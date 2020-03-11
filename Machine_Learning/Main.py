import sys

if __name__ == "__main__":
    print("\nPlease select algorithm:")
    print(" [1] Deep Q-Learning")
    print(" [2] Simple Evolutionary")
    print(" [3] NEAT")
    print(" [4] GNARL")
    print("([5] Render Net)")

    algorithm = input("--> ")

    if algorithm == '1':
        print("Running DeepQ.py main...\n")
        sys.path.insert(1, 'DeepQ')
        import DeepQ
        DeepQ.main()
    elif algorithm == '2':
        print("Running SimpleE.py main...\n")
        sys.path.insert(1, 'SimpleE')
        import SimpleE
        SimpleE.main()
    elif algorithm == '3':
        print("Running NEAT.py main...\n")
        sys.path.insert(1, 'NEAT')
        import NEAT
        NEAT.main()
    elif algorithm == '4':
        print("Running GNARL.py main...\n")
        sys.path.insert(1, 'GNARL')
        import GNARL
        GNARL.main()
    elif algorithm == '5':
        import Unity
        Unity.render(input("Neural net: "))
