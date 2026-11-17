# Knowledge Base GUI (Tkinter)

A Python Tkinter app that stores facts as predicates, such as `Professor(Lucy)` or `Likes(John, Susie)`, and answers queries about them.

## Features
- Add, delete and list facts
- TRUE / FALSE queries, and wildcard queries such as `Parent(John, ?)`
- Predicate table showing each predicate, its number of arguments and its meaning
- Save and load facts from a text file

## How to run
    sudo apt install python3-tk
    python3 knowledge_base_app.py

`facts.py` is a simpler version of the same idea that uses only Python sets.
`Tkinter_Knowledge_Base_Project.pptx` is the project presentation.
