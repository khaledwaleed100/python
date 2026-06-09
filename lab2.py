import random


def reduce_adjacent(lst):
    if not lst:
        return []
    result = [lst[0]]
    for i in range(1, len(lst)):
        if lst[i] != lst[i-1]:
            result.append(lst[i])
    return result

def front_back(a, b):
    a_mid = (len(a) + 1) // 2
    b_mid = (len(b) + 1) // 2
    a_front, a_back = a[:a_mid], a[a_mid:]
    b_front, b_back = b[:b_mid], b[b_mid:]
    return a_front + b_front + a_back + b_back


def all_different(seq):
    return len(seq) == len(set(seq))


def bubble_sort(lst):
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

# 5. Guessing Game
def guessing_game():
    while True:
        target = random.randint(1, 100)
        tries = 10
        guessed_numbers = set()
        
        print("\n--- New Game Started ---")
        print("I have generated a random number between 1 and 100.")
        
        while tries > 0:
            try:
                guess = int(input(f"Guess the number (Tries left: {tries}): "))
            except ValueError:
                print("Please enter a valid integer.")
                continue
                
            if guess < 1 or guess > 100:
                print("Not allowed! Number is out of range (1-100). Try again.")
                continue
                
            if guess in guessed_numbers:
                print("Hint: You already guessed that number! Try a different one.")
                continue
                
            guessed_numbers.add(guess)
            tries -= 1
            
            if guess == target:
                print("Congratulations! You guessed the correct number.")
                break
            elif guess < target:
                print("Hint: Your guess is smaller than the random number.")
            else:
                print("Hint: Your guess is bigger than the random number.")
                
        if tries == 0 and guess != target:
            print(f"You're out of tries! The correct number was {target}.")
            
        replay = input("Do you want to play again? (y/n): ")
        if replay.lower() != 'y':
            print("Thanks for playing!")
            break


def diagonalDifference(arr):
    n = len(arr)
    primary_diagonal = sum(arr[i][i] for i in range(n))
    secondary_diagonal = sum(arr[i][n - i - 1] for i in range(n))
    return abs(primary_diagonal - secondary_diagonal)