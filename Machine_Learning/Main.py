import sys

if __name__ == "__main__":
    print(".___  ___.      ___       ______  __    __   __  .__   __.  _______     __       _______     ___      .______      .__   __.  __  .__   __.   _______ \n|   \/   |     /   \     /      ||  |  |  | |  | |  \ |  | |   ____|   |  |     |   ____|   /   \     |   _  \     |  \ |  | |  | |  \ |  |  /  _____|\n|  \  /  |    /  ^  \   |  ,----'|  |__|  | |  | |   \|  | |  |__      |  |     |  |__     /  ^  \    |  |_)  |    |   \|  | |  | |   \|  | |  |  __  \n|  |\/|  |   /  /_\  \  |  |     |   __   | |  | |  . `  | |   __|     |  |     |   __|   /  /_\  \   |      /     |  . `  | |  | |  . `  | |  | |_ | \n|  |  |  |  /  _____  \ |  `----.|  |  |  | |  | |  |\   | |  |____    |  `----.|  |____ /  _____  \  |  |\  \----.|  |\   | |  | |  |\   | |  |__| | \n|__|  |__| /__/     \__\ \______||__|  |__| |__| |__| \__| |_______|   |_______||_______/__/     \__\ | _| `._____||__| \__| |__| |__| \__|  \______| ")

    print("\nPlease select algorithm:")
    print(" [1] Deep Q-Learning")
    print(" [2] Simple Evolutionary")
    print(" [3] NEAT (neat-python)")
    print(" [4] NEAT (Sam)")
    print(" [5] GNARL")
    print("([6] Render Net)")
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
        print("Running NEAT-python.py main...\n")
        sys.path.insert(1, 'NEAT')
        import NEAT_Python
        NEAT_Python.main()
    elif algorithm == '4':
        print("Running NEAT-Sam.py main...\n")
        sys.path.insert(1, 'NEAT')
        import NEAT_Sam
        NEAT_Sam.main()
    elif algorithm == '5':
        print("Running GNARL.py main...\n")
        sys.path.insert(1, 'GNARL')
        import GNARL
        GNARL.main()
    elif algorithm == '6':
        import Unity
        Unity.render(input("Neural net: "))
