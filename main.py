import time
import turtle
import pandas


# Gives the user feedback when they have guessed the same state twice
def repetition(message):
    message.hideturtle()
    message.penup()
    message.goto(0, 300)
    message.write("Repeated State...", align="center", font=("Arial", 60, "normal"))


# Clears various user feedback calls to allocate screen space for new calls
def hide_error_message(t):
    t.clear()


# Gives the user feedback when they guess an incorrect state that is not correct spelling
def incorrect_state_message(message):
    message.hideturtle()
    message.penup()
    message.goto(0, 300)
    message.write("Not a State...", align="center", font=("Arial", 60, "normal"))


# Gives the user positive feedback and further lets them know they have guessed a correct state
def correct_state_message(message):
    message.hideturtle()
    message.penup()
    message.goto(0, 300)
    message.write(f"Correct: {user_state}", align="center", font=("Arial", 60, "normal"))


# Writes in the correctly guessed state within our empty states map
def fill_state(message):
    message.hideturtle()
    message.penup()
    message.goto(coordinate)
    message.write(user_state)


STATES = 50
# holds the users guesses to validate for success, repeat, and failure
guessed_states = []
screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
# Loads in the image to be able to be used by a turtle
screen.addshape(image)
# Turtle uses the image, and then it will be displayed
turtle.shape(image)
screen.tracer(0)
# Used for unsuccessful guess feedback
validate = turtle.Turtle()
# Used for repetition feedback
rep = turtle.Turtle()
# Used for successful guess feedback
s = turtle.Turtle()
# Used for writing the state in the proper location
tim = turtle.Turtle()
# Utilizes the pandas library to easily take in data from a csv file
data = pandas.read_csv("50_states.csv")
# Keeps track of how many successful guesses the user has
count = 0

while count < STATES:
    screen.update()
    time.sleep(0.1)
    # Creates the textbook to receive user input
    user_state = screen.textinput(title=f"{count} out of 50", prompt="Enter 'exit' to quit...\nEnter another state:")
    # Guarantees a capitalized state to compare to dataframe
    user_state = user_state.capitalize()
    if user_state == "Exit":
        break
    # Boolean to validate guess
    test_state = False
    # Checks each state to see if a guess is an actual state
    for state in data.state:
        if state == user_state:
            test_state = True
    # If the guess is not a state, we give feedback to the user and refrain from checking for duplicate and insertion
    if not test_state:
        hide_error_message(rep)
        hide_error_message(s)
        incorrect_state_message(validate)
    else:
        hide_error_message(validate)
        hide_error_message(s)
        # Boolean to check for a repeated guess
        test_repeat = True
        # We compare the guess to the user guess array to make sure it is not repeated
        for guess in guessed_states:
            if guess == user_state:
                test_repeat = False
        # Gives user feedback that they have already made that guess
        if not test_repeat:
            repetition(rep)
        # Once we know it is not a duplicate, then we know at this point that the guess is a state and that it is not
        # repeated. This means that the guess is a success, and we can write to the screen and update the guessed count
        else:
            hide_error_message(rep)
            hide_error_message(s)
            correct_state_message(s)
            guessed_states.append(user_state)
            # Pandas library is used to quickly index the coordinate that we need to fill in our states image
            state_xcor = data.x[data.state == user_state].to_list()
            # The previous line receives the y input as an array, when we need a single variable; this fixes that
            x = state_xcor[0]
            state_ycor = data.y[data.state == user_state].to_list()
            y = state_ycor[0]
            # We combine coordinates to make a simplified goto() call
            # The coordinates are what allows the turtle to know where to fill in the correct state.
            # The x and y coordinates are predetermined to roughly have each state in the proper position
            coordinate = [x, y]
            # Fills in the state on the map
            fill_state(tim)
            # Increments the successfully guessed state count
            count += 1

# We collect the data on which states the user has failed to guess
missing_states = []
# We loop through the full states list, and if the state does not exist in the
# user guest list, then we add that state to the missing state array
for state in data.state:
    if state not in guessed_states:
        missing_states.append(state)
# We then convert the array to a pandas DataFrame
missing_states_data = pandas.DataFrame(missing_states)
# Then we convert the DataFrame into a CSV so that the user can easily see which states need to be learned
# See the CSV file for example
missing_states_data.to_csv("states_to_learn.csv")

