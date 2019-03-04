# Faris Nassif
# Shunting Yard Algorithm

def shunt(infix):

    specials = {'*': 50, '.': 40, '|': 30}

    # Equivelant postix regular expression
    pofix = ""
    # Stack of operators 
    stack = ""

    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            # Character at last index of stack
            while stack[-1] != '(':
                # Pofix String = whatever was there + last index of stack
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            pofix = pofix + c 

    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]

    return pofix

print(shunt("(a*b.c|b.b.c*|b*.b*.c)")) 