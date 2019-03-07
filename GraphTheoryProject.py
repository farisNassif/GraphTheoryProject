# Faris Nassif
# Shunting Yard Algorithm

def shunt(infix):
    # Defining a list of special characters and giving them a value based on their precedence
    # https://www.youtube.com/watch?v=B72XAeFO9ZE At 47:10 the video goes over precedence and operators
    # This was pretty helpful to me when trying to understand the program
    specials = {'*': 50, '+':40, '?':30,'.':20, '|':10}
    # * = The preceding item will be matched zero or more times
    # + = The preceding item will be matched one or more times
    # ? = Matching 0 or 1 times
    # . = Concatenate, a.b | a followed by a b
    # | = Or, a.b | c.d   Either is accepted
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
# Just printing an infix expression and the same expression in postfix
print("Infix\na.b*|b+a.d*\nPostfix") 
print(shunt("a.b*|b+a.d*")) 

# Prompting the user to input an expression of their own 
regexp = str(input("Enter a regular expression in infix notation: "))
print(shunt(regexp)) 