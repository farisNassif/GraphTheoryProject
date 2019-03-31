# Faris Nassif
# Third Year Graph Theory Project

# The goal of this Program is to develop a Python script that will 
# construct an NFA from a regular expression in Polish notation and 
# see if the regular expression matches a certain String with help 
# from the previously constructed NFA.
import sys
import os
from datetime import datetime

# Represents a state with two arrows, labelled by label
# Use none for a label representing 'e' arrows
class state:
    label = None
    edge1 = None
    edge2 = None

# NFA represented by initial and accept states
class nfa: 
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

# Shunting Yard Algorithim
# -- Resources I found helpful upon researching the algorithim --
# At 47:10 the video goes over precedence and operators - https://www.youtube.com/watch?v=B72XAeFO9ZE
# Helped visualise the process - http://www.oxfordmathcenter.com/drupal7/node/628 
# http://spronck.net/pythonbook/pythonbook.pdf page 279. Assisted with Operators
def shuntingYard(infix):
    """Return a postfix regular expression that was previously infix"""
    # Defining a list of special characters and giving them a value based on their precedence
    specials = {'*': 50, '+':40, '?':30, '$':25, '.':20, '|':10}
    # * = The preceding item will be matched zero or more times
    # + = The preceding item will be matched one or more times
    # ? = Matching 0 or 1 times. For exmaple (a.b.c.d?) Will match abc | abcd
    # $ = Character doesn't appear, similar to != also matches empty string
    # Matches the end of a String, a.b$ should match a for exmaple. Also matches the empty string
    # Equivelant postix regular expression
    pofix = ""
    # Stack of operators 
    stack = ""
    # Going through each character input by the user
    for c in infix:
        if c == '(':
            stack = stack + c
        # When a corresponding closing bracket is seen
        elif c == ')':
            # While the character at last index of stack is '(' indicating a new 
            while stack[-1] != '(':
                # Pofix String = whatever was there + last index of stack
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
        # If the character being read is a special character (as defined)
        elif c in specials:
            # While stack is not empty, and while c's precedence is <= than the last
            # operator on the stack, take highest precedence operator off the stack and 
            # push it to pofix
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            # If its not a special char or bracket add it to postfix
            pofix = pofix + c
    while stack:
        # Take whatevers on the end of the stack and put it into pofix
        # Then get rid of it on the stack
        pofix, stack = pofix + stack[-1], stack[:-1]
    return pofix

# Thompson's Construction
# -- Resources I found helpful when researching Thompson's Construction --
# Helped cement the process a bit better - https://www.youtube.com/watch?v=RYNN-tb9WxI
# https://en.wikipedia.org/wiki/Thompson%27s_construction
def compile(pofix):
    """Constructs NFA's and pushes them to the stack"""
    nfastack = []
    for char in pofix:
        if char == '.':
            # . operator needs two operands, pops two of them from the stack 
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Connect the first nfas accept to the second initial
            nfa1.accept.edge1 = nfa2.initial
            # Push it to the stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        elif char == '+':
            # Pop a single nfa from the stack
            nfa1 = nfastack.pop()
            # With the '+' operator, there is no need to create new initial or accept states
            nfa1.initial.edge1 = nfa1.accept
            nfa1.accept.edge1 = nfa1.initial
            # Push new nfa to the stack
            newnfa = nfa(nfa1.initial, nfa1.accept)
            nfastack.append(newnfa)
        elif char == '|':
            # | operator needs two operands, pops two of them off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Create a new initial state, connect it to initial states
            # of the two nfa's popped form the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # Create a new accept state, connecting the accept states
            # of the two nfa's popped from the stack to the new state
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge2 = accept
            # Push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        elif char == '?':
            # Pop a single nfa from the stack
            nfa1 = nfastack.pop()
            # New initial
            initial = state()
            # Only need two states and two arrows with the '?' operator
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa1.accept
            # Push new nfa to the stack
            newnfa = nfa(initial, nfa1.accept)
            nfastack.append(newnfa)
        elif char == '*':
            # Pop a single nfa from the stack
            nfa1 = nfastack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join new intial state to nfa1's intial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Join the old accept state to the new accept state and nfa1's intial state 
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # Push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        elif char == '$':
            # C$ should match the empty string, C.B$ should match C etc. Kinda like c NOT followed by b returns true
            # Pop a single nfa from the stack
            nfa1 = nfastack.pop()
            # New initial and new accept
            initial = state()
            accept = state()
            # Match new initial with old initial and old accept with new accept
            initial.edge1 = nfa1.initial
            nfa1.accept.edge1 = accept
            # Match new accept with old initial
            accept = nfa1.initial
            # Push to stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        else:
            # Two 'circles', initial and accept
            accept = state()
            initial = state()
            # Joining by arrow labelled by the character, whatever it is
            initial.label = char
            initial.edge1 = accept
            # Point to the accept state
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
    # Should only have a single nfa on it         
    return nfastack.pop()

def followes(state):
    """Return the set of states that can be reached from state following the e arrows"""
    # Create a new set with state as it's only member
    states = set()
    states.add(state)

    # Check if state has arrows labelled e from it
    if state.label is None:
        # Check if edge1 is a state
        if state.edge1 is not None:
            # If there's an edge1, follow it
            states |= followes(state.edge1)
        # Check if edge2 is a state
        if state.edge2 is not None:
            # If there's an edge2, follow it
            states |= followes(state.edge2)
    
    # Return the set of states
    return states

def match(infix, string):
    """Matches the string to the infix regular expression"""
    # Shunt and compile the regular expression
    postfix = shuntingYard(infix)
    # Builds the NFA
    nfa = compile(postfix)

    # The current set of states and the next set of states
    current = set()
    nexts = set()

    # Add the initial state to the current list
    current |= followes(nfa.initial)

    # Loop through each character in the string
    for s in string:
        # Loop through the current set of states
        for c in current:
            # Check if that state is labelled s
            if c.label == s:
                # Add the edge1 state to the next set.
                nexts |= followes(c.edge1)
        # Set current to next, and clear out next 
        current = nexts
        nexts = set()
    # Check if the accept state is in the set of current states
    return (nfa.accept in current)

def runner():
    """Used to run the program and call other funtions methodically"""
    # Printing information messages
    print(f"\n--- Author: Faris Nassif | G00347032 | {sys.argv[0]} ---\n") 
    # Defined var for controlling user input
    userOption = "traverse"
    # This is solely for file output purposes, shows how many times user has looped
    iteration = 1

    # Functions like a do:while, user can traverse the program until they want to exit
    while userOption != "exit":
        # Will be populated by the user
        infixes = []
        # Strings to compare against, you can change them to whatever if you'd like to test certain expressions
        strings = ["abc","abcd","abbbbbccc","abbbc", "", "a"]
        # Just setting it to 999 so the while below actually functions properly
        regExpAmt = 999
        # While RegExp amount is 1-5
        while regExpAmt > 5 or regExpAmt < 1:
            regExpAmt = int(input("Choose how many Regular Expressions you wish to enter (Up to 5): "))
        # Strings to compare against to have in mind when writing your Regular Expression
        print("\nStrings to compare against. Keep these in mind when writing your Exp - ", strings)
        # Information message to the user        
        print("\n*An example of a regular expression could be (a.b.c?)|(a+.b*)") 
        # Will loop n times depending on users choice from previous input
        for i in range(regExpAmt):
            # Adding n regular expressions to infixes[]
            infixes.append((input("Please enter Regular Expression " + str(i+1) + ": ")))  
        # Create a file called regexp.txt if it does not exist
        f = open("regexp.txt", "a")
        # Making use of datetime import, outputting current date in file to user
        now = datetime.today().isoformat()
        # Writing Iteration number and time + date to the file
        f.write("-- Iteration [%i] | %s --\n" % (iteration, now))
        # If the user decides to reloop they won't get confused at what piece of data in the .txt file belongs to which iteration
        iteration = iteration + 1
        # Setting this var to 0 again so I can print the regexp number in the file
        regExpAmt = 0
        for i in infixes:
            # regExpAmt++ just didn't want to work
            regExpAmt = regExpAmt + 1
            for s in strings:
                # Also write the result to a file
                f.write("Regular Expression[%i]: %s --> %s | Match Result --> %s\n" % (regExpAmt, i, s, match(i,s)))     
        # Closing the file      
        f.close()
        # If user chooses to re-run the program they may without having to run it again in the console
        userOption = input("Type exit to termiante the program and view the Results or ANY other key to continue: ")
# Runs the script
runner()
print(shuntingYard("(a+.b)"))
print("\nPlease take a look at the Github Wiki in regards to the '$','+' and '?' operators") 
# Pops open the file with results of the matching
os.startfile("regexp.txt")