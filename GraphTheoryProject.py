# Faris Nassif
# Third Year Graph Theory Project

# The goal of this Program is to develop a Python script that will 
# construct a NFA from a regular expression in Polish notation and 
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
            # Alike the * operator, takes one operand 
            # Pop a single nfa from the stack
            nfa1 = nfastack.pop()
            # Create new initial state
            initial = state()
            # Join new intial state to nfa1's intial state
            initial.edge1 = nfa1.initial
            nfa1.initial.edge1 = accept
            # Join the accept state to the old initial 
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # Push new nfa to the stack
            newnfa = nfa(initial, nfa1.accept)
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
            # Join new intial state to nfa1's intial state and the new accept stae
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

print("---Author: Faris Nassif | G00347032---\n") 

# Just printing an infix expression and the same expression in postfix to test
print("Infix\n(a.b)*|(b+a.d*)\nPostfix") 
print(shuntingYard("(a.b)*|(b+a.d*)")) 

# Prompting the user to input an expression of their own for testing purposes
regexp = str(input("Enter a regular expression in infix notation: "))
print(shuntingYard(regexp)) 
