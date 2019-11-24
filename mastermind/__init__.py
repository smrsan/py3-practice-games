from utils import clear_term


def mastermind_game():
    while True:
        clear_term()
        play_again = True
        first_user_input = input('Enter numbers (separated by space): ')
        first_user_input = first_user_input.split(' ')
        clear_term()
        while True:
            guess_input = input("Guess numbers: ")
            guess_input = guess_input.split(" ")
            result = []
            guess_word_index = -1
            correct_words_len = 0
            for guess_word in guess_input:
                guess_word_index += 1
                color = 3
                if guess_word in first_user_input:
                    color = 2
                    if guess_word_index == first_user_input.index(guess_word):
                        color = 1
                        correct_words_len += 1
                result.append(str(color))
            result = ', '.join(result)
            print(f'result: {result}')
            if correct_words_len == len(first_user_input):
                print('You WON!!!')
                while True:
                    ans = input('Do you wanna play again? (yes/no): ')
                    if ans.lower() == 'no':
                        play_again = False
                        break
                    elif ans.lower() == 'yes':
                        play_again = True
                        break
                break

        if not play_again:
            break
