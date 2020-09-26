"""
File name: prime_detector.py
Creator: Joshua Hall
File description: Determines whether or not an input number is prime or not. Results are displayed to the console.
"""

print('Welcome!\nEnter a number to see if it is prime!\nPress \'Q\' to exit.')
input_num = input('Enter a number: ')
while input_num.lower() != 'q':  # run loop until 'Q' or 'q' are entered
    if not input_num.isnumeric():  # validate input
        print('Invalid Input. Please enter an integer between 0 and 100.')
    else:
        input_num = int(input_num)
        for num in range(2, input_num):  # perform modulus on every number from 2 until the number below the input
            if (num < input_num and input_num % num == 0) or input_num in (0, 1):  # 0&1 are not prime by definition
                print('The number is not prime.\n\nEnter another number or press \'Q\'.')
                break  # break the for loop
        else:
            print('The number is prime.\n\nEnter another number or press \'Q\'.')
    input_num = input('Enter a number: ')  # prompt the user for another input
print('{}\nExiting Program.'.format('-' * 60))
