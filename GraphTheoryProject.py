# Faris Nassif
# Third Year Graph Theory Project

# The goal of this Program is to develop a Python script that will 
# construct an NFA from a regular expression in Polish notation and 
# see if the regular expression matches a certain String with help 
# from the previously constructed NFA.

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
def shuntingYard(infix):
    """Return a postfix regular expression that was previously infix"""
    # Defining a list of special characters and giving them a value based on their precedence
    specials = {'*': 50, '+':40, '?':30,'.':20, '|':10}
    # * = The preceding item will be matched zero or more times
    # + = The preceding item will be matched one or more times
    # ? = Matching 0 or 1 times

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

print("---Author: Faris Nassif | G00347032---") 
print("Regular Expression Program (change this later)\n") 
# Defined vars for controlling user input
userOption = "traverse"

# Functions like a do:while, user can traverse the program until they want to exit
while userOption != "exit":
    regexp = str(input("Please enter a regular expression: "))

    userOption = input("Type exit to termiante the program or any other key to continue: ")

infixes = ["1*|3+"]
strings = ["1111111111","3"]

for i in infixes:
    for s in strings:
        print(match(i,s), i, s)



# Just printing an infix expression and the same expression in postfix to test
# print("Infix\n(a.b)*|(b+a.d*)\nPostfix") 
# print(shuntingYard("(a.b)*|(b+a.d*)")) 

# Prompting the user to input an expression of their own for.. testing purposes
# regexp = str(input("Enter a regular expression in infix notation: "))
# print(shuntingYard(regexp)) 
