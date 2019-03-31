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

_There are some references not mentioned here but that are refereced in the actual code where they would be relevant_