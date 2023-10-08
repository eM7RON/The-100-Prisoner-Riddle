from tqdm import tqdm

import numpy as np

import joblib
import time

def create_game() -> np.array:
    """
    Create and return a game board.
    
    Generate a shuffled array of numbers from 1 to 100 and reshape it into a 10x10 matrix.
    
    Returns:
        np.array: A 10x10 matrix where each cell contains a unique number from 1 to 100.
    """
    numbers = np.arange(1, 101)
    np.random.shuffle(numbers)
    return numbers.reshape(10, 10)

def get_index(n: int) -> tuple:
    """
    Retrieve the matrix index of a given number.
    
    Args:
        n (int): A number whose index in the matrix is to be retrieved.
    
    Returns:
        tuple: A tuple containing the row and column index of the number in the matrix.
    """
    return lookup[n]
    
def play() -> int:
    """
    Simulate a single round of the game.
    
    Each prisoner starts by opening the box with their number and then follows a looping path, 
    opening the box of the number they found in the previous box. 
    
    Returns:
        int: 0 if the loop size exceeds 50, otherwise 1.
    """
    game = create_game()

    for prisoner in range(1, 101):
        current_number = prisoner
        loop_size = 1
        
        while True:
            number_in_box = game[get_index(current_number)]
            if number_in_box == prisoner:
                break

            loop_size += 1

            if loop_size > 50:
                return 0

            current_number = number_in_box
            
    return 1


# Number of rounds to simulate
n = 1000000

# Matrix representing the numbers from 1 to 100
boxes = np.arange(1, 101).reshape(10, 10)

# A dictionary for O(1) lookup of matrix indices given a number
lookup = {boxes[i, j]: (i, j) for i in range(10) for j in range(10)}

# A generator that will run each game instance
runner = (joblib.delayed(play)() for _ in tqdm(range(n)))

# Record the start time for performance measurement
start = time.time()

# Run the game instances in parallel
results = joblib.Parallel(n_jobs=-1)(runner)

# Calculate elapsed time
end = time.time()

# Calculate the success percentage
percentage_success = sum(results) / len(results) * 100

print(f"{n} runs in {round(end - start)} seconds\n{round(percentage_success, 5)}% succeeded")
