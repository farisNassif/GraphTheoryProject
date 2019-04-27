# NFA Regular Expression Matcher
This is a project for 3rd Year Software Development module Graph Theory, using the Python Programming Language to construct Non-Deterministic Finite Automata based on Postfix Regular Expressions and attempt to match them with Strings.

I have included a detailed account of decisions made and design logic behind the Script, as well as some suggested Input to test all included Operators and other relevant information in this README.

## Goals 
The goal of this Project is to convert a Regular Expression in Infix to Postfix using [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) and to then build Non-Deterministic Finite Automata using [Thompson's Construction](https://en.wikipedia.org/wiki/Thompson%27s_construction). Once the NFA's are built they may then be used to compare the Regular Expression to a certain String.

## Research
Before I had written any code I had attempted to construct a rough idea of how the Script should run on paper. The method I had in mind followed the same structure that I ultimately ended up with. It was essentially [Infix RegExp] --> [Postfix Regexp] --> [Construct Small NFA's] --> [Add to Stack] --> [Perform String Matching]. However I was completely lost on how to actually implement these main functions especially in Python. I started watching the material available on Learnonline which helped me get a rough idea of the techniques involved. I then tried to find independent sources of information. Below is a list of sources I gathered information from during the timeline of this project and how that information helped shape my implementation. 

[Regular Expression to NFA](https://www.youtube.com/watch?v=RYNN-tb9WxI) - This was I believe the first video I watched, it really helped to further cement the concept of constructing NFA's from Regular Expressions.

[Oxford Math Center: Shunting Yard](http://www.oxfordmathcenter.com/drupal7/node/628) - This article helped me to visualise how one may push and pop a Postfix Expression to and from a Stack and how to interact with the Postfix Expression after it's been pushed to the Stack.

[The Coder's Apprentice (Specifically page 279-282)](http://spronck.net/pythonbook/pythonbook.pdf) - I didn't have much time to read all of this book however this specific page along with some others did stick out at me more than others. It gave me a further understanding of previously unknown operators (to me) such as the '$', '?' and '+' operator and how they interact with their predecessing operands.

[Operator Precedence](https://www.boost.org/doc/libs/1_56_0/libs/regex/doc/html/boost_regex/syntax/basic_extended.html#boost_regex.syntax.basic_extended.operator_precedence) - The order of Precedence of the Operators I had planned to implement was completely unknown to me, reading through this helped me to understand the order I should implement them and why.

[Regular Expressions to C Code](https://www.cs.york.ac.uk/fp/lsa/lectures/REToC.pdf) - Even though the Project was assigned to be written in Python reading through this PDF which was intended for NFA construction with C it did help visualise the whole process. The way it's performed in these slides is slightly different, instead of constructing NFA's from Regular Expressions DFA's are build from the NFA's built from the Regular Expressions. Even still it helped cement the whole process a bit better for me.

*_There are some references not mentioned here but that are refereced in the actual code where they would be relevant_

## Script Design and functionality
The script itself is ran from the `runner()` function. The idea behind this funtion was to act as a capsule that would execute all other functions of the script. The unique characteristics of this function is that it first asks the user to enter how many Regular Expressions they wish to enter(Up to 5). The input is completely validated so while n != 1-5 the user will continue to loop until a valid input is provided. The Script then prompts for n Regular Expressions to be entered. The Expressions can be entered in either Infix or Postfix Notation, either way the Expression will be stored as Postfix.

Once the Infix Regular Expression is input it gets stored in `infixes []`. Another list `strings []` is defined and is used to compare the Regular Expressions against. I had planned to have the values in the `strings []` list input by the User however I felt it would make more sense to have them hardcoded as it makes it a lot easier to demonstrate the program funtionality. 

The first major point of the `runner()` function is when the `match(x,x)` function is invoked. The `match(x,x)` function takes two arguments, the `infixes []` and `strings []` lists. Once inside the `match(infixes[], strings[])` function `shuntingYard(x)` is then invoked. It takes one argument which is the list of Infix Expressions. 

The purpose of the `shuntingYard(infixes[])` function is to convert the passed in Infix Expression to Postfix. For each character in the Infix Regular Expression a for loop is executed that has different conditions depending on whether the character read is a round bracket, a character or a previouly declared special operator. For example take the Infix Expression (a.b), the first character read will be the '(' so '(' will be pushed to the previously declared `stack`. The next character to be read would be 'a', which is neither a round bracket or previously declared special character so 'a' is then stored in `pofix`. The next character '.' which is a special character is then read, it's precedence is then checked and then the character gets pushed to `stack`. So currently on the stack we have '(', '.' and on `pofix` we have 'a'. When the final two characters 'b' and ')' are read the function omitts the round brackets and pushes the operators to `pofix` which should just have 'ab' on it right now. The operator that was read '.' requires two operands so it is placed in front of the b like so 'ab.'. If the Expression was for example 'a+.b' the '+' operator requires one operand while '.' requires two so the Postfix version of this Expression would be 'a+b.'. Once `pofix` is populated with the Postfix Regular Expression 'a.b' it is returned by the function back to `match(x,x)`.

The next step of the Script is to construct a Non-Deterministic Finite Automata based on the Postfix Expression 'a.b'. Within `match(x,x)` there is a call to the `compile(postfix)` funtion which accepts a Postfix Regular Expression as an argument and constructs an NFA based on the Expression. It reads the Expression character by character and creates small NFA's that will amalgamate into a larger one when returned. Each normal character read so 'a' or 'b' will translate to an NFA with two states, an initial and and an accept state with one edge from the initial to the accept. Depending on the Operator read that state will be expanded and have edges added to it. I'll explain this function more thoroughly in another segment of this document with reference to diagrams.

Once the expression is translated to an NFA it is then returned back to `match(x,x)`. The `followes(state)` function is the invoked which takes in the initial state of the returned NFA. This function returns a set of states that can be reached by following the 'e' arrows. `match(x,x)` then loops for each character in the `strings[]` argument and then loops within that n times depending on what was returned by `followes(state)`. It checks to see if what was returned matches the currently read `strings[]` character, if it does add the edge1 state to the next set. Do this for every character and return a boolean based on if the accept state is in the set of current states.

The `match(x,x)` function at this point has run it's course and returns a boolean value back to `runner()`. If the given String was 'ab' the Regular Expression '(a.b)' would return a true on that String, in this case if it was anything else it would return a false. This is done for all n Regular Expressions entered by the user and compared against all hardcoded Strings. It's then formatted and written to a file.

No output actually appears in the console, all output is written to the 'regexp.txt' file which, if not already created will be created upon running the program. Since the user can choose to loop over the program an Iteration number is shown at the top of each Iteration in the file along with the date and time that Iteration was written to the file.

Finally when 'exit' is input into the console, the file will pop up for the user automatically using the `os` import displaying the results of all their matching.

Then the function works on the second paramater passed into it `strings[]`. 

## Examples of running the Program
Once ran (_python graphtheoryproject.py_) 

![alt text](https://i.imgur.com/CrbLeOF.png "Two iterations")

Once 'exit' is input a text file will pop out with the results of the attempted matching.

![alt text](https://i.imgur.com/nAvymXf.png "Results")

A file then automatically pops up displaying the results. It additionally shows the iteration number, date and time and the corresponding number of the regualr expression based on which order it was entered in.

## Added Operators and how they influence NFA Construction
_The following NFA were constructed by me on http://madebyevan.com/fsm/_

<b>*(_NI = New Initial, NA = New Accept, I = Initial, A = Accept_)</b>\
\
The first of the new Operators I implemented was the '+' Operator. The '+' Operator indicates a character matching 1 or more times

_Given the Regular Expression '(a+)'_
![alt text](https://i.imgur.com/YqUbrzt.png "+ Operator")

Take the Regular Expression (a.b+). This will match 'ab', 'abbbbb....' but not 'a' since it doesn't accept the empty string.
**
The Next Operator I implemented was the '?' Operator. The '?' Operator indicates a character has matched 0 or 1 times.

_Given the Regular Expression '(a?)'_
![alt text](https://i.imgur.com/PBldbjw.png "? Operator")

Take the Regular Expression(a.b?). This will match 'a','ab' but nothing else, since it's a binary operator, 0 or 1 theres only two outcomes
**
The Next Operator I implemented was the '$' Operator. The '$' Operator indicates a character has matched 0 times. 

_Given the Regular Expression '(a$)'_
![alt text](https://i.imgur.com/cRMXQqD.png "$ Operator")

Take the Regular Expression(a.b$). This will match ONLY 'a'. or (a$) will match the empty string.

## Testing Operators
I will input Regular Expressions that will test against the `Strings["abbbaaaccaa","a",""]`


![alt text](https://i.imgur.com/iYuQDTM.png "Testing Operators")

The operators correctly match all corresponding Strings

## Conclusion
Overall the Project has been a huge learning experiences. From concepts I've never heard of and a Programming Language we've not even used so far in the course I can confidently say I've expanded my skillset during the timeline of the project. If I was to start the Project again I'd love to do it in another Programming Language, C preferably and I would definitely give myself more time to research the topics. With the Projects related topics it was actually pretty hard to find good content online that wasn't poorly orchestrated or conveyed, my research pretty much spans the links I've provided along with books and links posted on the course page which helped immensely with the creation of the end product of this project. If I had more time I would sit down and focus on other operators and try and fix up the '$' operator. I feel the way I did it wasn't optimal. If need be I have all my notes and documents and will bring them to the demonstration if necessary.
\
\
_Faris Nassif - G00347032@gmit.ie_








