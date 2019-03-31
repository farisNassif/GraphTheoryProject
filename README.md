# NFA Regular Expression Matcher
This is a project for 3rd Year Software Development module Graph Theory, using the Python Programming Language to construct Non-Deterministic Finite Automata based on Postfix Regular Expressions and attempt to match them with Strings.

The [https://github.com/farisNassif/GraphTheoryProject/wiki/Design-Document](Design Document) contains a detailed account of decisions made and design logic behind the Script, as well as some suggested Input to test all included Operators.

###### Goals 
The goal of this Project is to convert a Regular Expression in Infix to Postfix using [https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm](Dijkstra's algorithm) and to then build Non-Deterministic Finite Automata using [https://en.wikipedia.org/wiki/Thompson%27s_construction](Thompson's Construction). Once the NFA's are built they may then be used to compare the Regular Expression to a certain String.