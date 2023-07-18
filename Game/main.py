import random
import os
import csv
from termcolor import colored

def get_main_directory():
    return os.path.dirname(os.path.abspath(__file__))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_profiles_file_path():
    return os.path.join(get_main_directory(), "profiles.csv")

def get_high_scores_file_path():
    return os.path.join(get_main_directory(), "gamedata.csv")

def check_dot(number):
    return number % 5 == 0

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def display_profiles():
    filename = get_profiles_file_path()
    profiles = []

    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                profiles = list(reader)
    except IOError:
        print(colored("Error: Failed to read profiles file.", "red"))

    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           Welcome to the Number Guessing Game!", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print("Existing Profiles:")

    if profiles:
        print(colored("Name", "cyan"))
        for i, profile in enumerate(profiles, start=1):
            print(f"{i}) {profile[0]}")

    print("0) Sign in with a new profile")

def create_profile(name):
    filename = get_profiles_file_path()
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name])
    except IOError:
        print(colored("Error: Failed to create profile.", "red"))

def remove_profile(name):
    filename = get_profiles_file_path()
    profiles = []

    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                profiles = list(reader)

        for profile in profiles:
            if profile[0] == name:
                profiles.remove(profile)

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(profiles)
    except (IOError, csv.Error):
        print(colored("Error: Failed to remove profile.", "red"))

def login_or_signin():
    display_profiles()

    if os.path.isfile(get_profiles_file_path()):
        choice = input(colored("\nEnter the number of your profile or '0' to sign in with a new profile: ", "yellow"))
        profiles_count = sum(1 for _ in open(get_profiles_file_path()))

        if choice.isdigit() and int(choice) in range(1, profiles_count + 1):
            try:
                with open(get_profiles_file_path(), 'r') as file:
                    reader = csv.reader(file)
                    profiles = list(reader)
                    return profiles[int(choice) - 1][0]
            except (IOError, csv.Error):
                print(colored("Error: Failed to read profiles file.", "red"))

    print(colored("You don't have a profile. Sign in with a new profile.", "red"))
    name = input(colored("Enter your name: ", "yellow"))
    create_profile(name)
    return name

def confirm_removal(name):
    confirm = input(colored(f"Are you sure you want to remove the profile '{name}'? (Y/N): ", "yellow"))
    return confirm.lower() == 'y'

def remove_profile_prompt():
    profiles = []
    if os.path.isfile(get_profiles_file_path()):
        try:
            with open(get_profiles_file_path(), 'r') as file:
                reader = csv.reader(file)
                profiles = list(reader)
        except (IOError, csv.Error):
            print(colored("Error: Failed to read profiles file.", "red"))

    if profiles:
        display_profiles()
        choice = input(colored("\nEnter the number of the profile you want to remove: ", "yellow"))

        if choice.isdigit() and int(choice) in range(1, len(profiles) + 1):
            profile_name = profiles[int(choice) - 1][0]
            if confirm_removal(profile_name):
                remove_profile(profile_name)
                print(colored(f"Profile '{profile_name}' removed successfully.", "green"))
                input(colored("\nPress Enter to continue...", "cyan"))
            else:
                print(colored("Profile removal canceled.", "yellow"))
                input(colored("\nPress Enter to continue...", "cyan"))
        else:
            print(colored("Invalid input. Profile removal canceled.", "red"))
            input(colored("\nPress Enter to continue...", "cyan"))
    else:
        print(colored("No profiles exist. Profile removal canceled.", "red"))
        input(colored("\nPress Enter to continue...", "cyan"))

def play_game(difficulty, player_name):
    clear_console()
    debug = True
    print(f"Please wait while the secret number is being generated.")
    secret_number = random.randint(1, 100)

    if difficulty == '1':
        while check_dot(secret_number):
            secret_number = random.randint(1, 100)
    elif difficulty == '2':
        while secret_number % 2 != 0:
            secret_number = random.randint(1, 100)
    elif difficulty == '3':
        while not is_prime(secret_number):
            secret_number = random.randint(1, 100)

    attempts = 0
    max_attempts = 0
    additional_feature = ''

    if difficulty == '1':
        max_attempts = 10
        additional_feature = "Extra Hint: The secret number is divisible by 5."
    elif difficulty == '2':
        max_attempts = 7
        additional_feature = "Additional Challenge: The secret number is divisible by 2."
    elif difficulty == '3':
        max_attempts = 5
        additional_feature = "Ultimate Challenge: The secret number is a prime number."

    difficulty_array = [colored('Easy', 'green'), colored('Normal', 'yellow'), colored('Hard', 'red')]
    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           Welcome to the Number Guessing Game!", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print("Try to guess the secret number.")
    print(f"Difficulty: {difficulty_array[int(difficulty) - 1]}")
    print(additional_feature)

    while attempts < max_attempts:
        user_guess = input("Take a guess: ")
        attempts += 1

        if user_guess == 'show' and debug == True:
            print(f"The number is: {colored(secret_number, 'green')}")
            continue

        try:
            user_guess = int(user_guess)
        except ValueError:
            print(colored("Error: Invalid input. Please enter a number.", "red"))
            attempts -= 1
            continue

        if user_guess == secret_number:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           Welcome to the Number Guessing Game!", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print(colored("Congratulations! You guessed the secret number.", "green"))
            print("Attempts left:", colored(max_attempts - attempts, "yellow"))
            save_player_data(player_name, attempts, difficulty)
            return attempts
        elif user_guess < secret_number:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           Welcome to the Number Guessing Game!", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("Try to guess the secret number.")
            print("Difficulty:", difficulty_array[int(difficulty) - 1])
            print(additional_feature)
            print(f'The secret number is {colored("higher than", "red")} {colored(user_guess, "blue")}')
        else:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           Welcome to the Number Guessing Game!", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("Try to guess the secret number.")
            print("Difficulty:", colored(difficulty_array[int(difficulty) - 1], "green"))
            print(additional_feature)
            print(f'The secret number is {colored("lower than", "red")} {colored(user_guess, "blue")}')

        if user_guess > 100 or user_guess < 1:
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           Welcome to the Number Guessing Game!", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("Try to guess the secret number.")
            print(f"Difficulty: {difficulty_array[int(difficulty) - 1]}")
            print(additional_feature)
            print("Number should be between 1 and 100. Try again.")
            attempts -= 1

        print("Attempts left:", colored(max_attempts - attempts, "yellow"))

    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           Welcome to the Number Guessing Game!", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print(colored("Game over! You ran out of attempts.", "red"))
    print("The secret number was:", colored(secret_number, "blue"))
    return 0

def update_high_score(player_name, score, difficulty):
    filename = get_high_scores_file_path()
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Score', 'Difficulty'])
            writer.writerow([player_name, score, difficulty])
    except (IOError, csv.Error):
        print(colored("Error: Failed to update high scores.", "red"))

def show_high_score(difficulty):
    filename = get_high_scores_file_path()
    high_scores = []

    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                high_scores = list(reader)
    except IOError:
        print(colored("Error: Failed to read high scores file.", "red"))

    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("           Welcome to the Number Guessing Game!", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print(f"High Scores for Difficulty {difficulty}:")
    if high_scores:
        print(colored("Name  |  Score", "cyan"))
        for score in high_scores:
            if score[2] == difficulty:
                print(f"{score[0]}  |  {score[1]}")
    else:
        print(colored("No high scores available.", "yellow"))

def save_player_data(player_name, score, difficulty):
    filename = get_high_scores_file_path()
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Score', 'Difficulty'])
            writer.writerow([player_name, score, difficulty])
    except (IOError, csv.Error):
        print(colored("Error: Failed to save player data.", "red"))

def main_menu(player_name="nonPlayer"):
    clear_console()
    print(colored("______________________________________________________", "cyan"))
    print(colored("          Welcome to the Number Guessing Game!", "yellow"))
    print(colored("______________________________________________________", "cyan"))
    print(f"You are logged in as {player_name}")
    print("\nSelect an option:")
    print(colored("1. Play Game", "green"))
    print(colored("2. High Score", "green"))
    print(colored("3. Exit", "green"))
    choice = input("\nEnter your choice (1-3): ")
    return choice

def start_game():
    player_name = login_or_signin()

    while True:
        choice = main_menu(player_name)

        if choice == '1':
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           Welcome to the Number Guessing Game!", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("Select difficulty:")
            print(colored("1. Easy", "green"))
            print(colored("2. Medium", "yellow"))
            print(colored("3. Hard", "red"))
            difficulty = input("\nEnter your choice (1-3): ")
            score = play_game(difficulty, player_name)
            if score > 0:
                update_high_score(player_name, score, difficulty)
            input(colored("\nPress Enter to continue...", "cyan"))
        elif choice == '2':
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           Welcome to the Number Guessing Game!", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("High Scores:")
            print(colored("1. Easy", "green"))
            print(colored("2. Medium", "yellow"))
            print(colored("3. Hard", "red"))
            difficulty = input("\nEnter the difficulty to see the high score (1-3): ")
            show_high_score(difficulty)
            input(colored("\nPress Enter to continue...", "cyan"))
        elif choice == '3':
            clear_console()
            print(colored("______________________________________________________", "cyan"))
            print(colored("           Welcome to the Number Guessing Game!", "yellow"))
            print(colored("______________________________________________________", "cyan"))
            print("Thank you for playing. Goodbye!")
            break
        elif choice == '4':
            remove_profile_prompt()

try:
    start_game()
except KeyboardInterrupt:
    clear_console()
    print("[ Goodbye!! ]")