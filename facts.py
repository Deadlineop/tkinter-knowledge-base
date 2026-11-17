# Facts and predicates represented with Python sets
#
#   Professor(Lucy)          -> "lucy" in professors
#   Male(Adam)               -> "adam" in males
#   Likes(John, Susie)       -> ("john", "susie") in likes
#   Parent(John, Adam)       -> ("john", "adam") in parents
#   Between(A, B, C)         -> ("a", "b", "c") in between

# ---------- 1-argument predicates (properties) ----------
professors = {"lucy", "danny"}
males = {"adam"}
students = {"ravi"}

# ---------- 2-argument predicates (relationships) ----------
likes = {("john", "susie")}
parents = {
    ("john", "adam"),
    ("mary", "susan"),
}

# ---------- 3-argument predicate ----------
between = {("a", "b", "c")}


# ---------- predicate functions ----------
def is_professor(person):
    return person.lower() in professors


def is_male(person):
    return person.lower() in males


def is_student(person):
    return person.lower() in students


def does_like(x, y):
    return (x.lower(), y.lower()) in likes


def is_parent(parent, child):
    return (parent.lower(), child.lower()) in parents


def is_between(x, y, z):
    return (x.lower(), y.lower(), z.lower()) in between


# ---------- queries with an unknown (like Parent(John, ?)) ----------
def children_of(parent):
    return [c for (p, c) in parents if p == parent.lower()]


def parents_of(child):
    return [p for (p, c) in parents if c == child.lower()]


if __name__ == "__main__":
    print("Parent(John, Adam):", ("john", "adam") in parents)
    print("Professor(Lucy):   ", "lucy" in professors)
    print("Professor(James):  ", "james" in professors)
    print()
    print("is_professor('Lucy')     =", is_professor("Lucy"))
    print("is_professor('James')    =", is_professor("James"))
    print("is_male('Adam')          =", is_male("Adam"))
    print("is_student('Ravi')       =", is_student("Ravi"))
    print("does_like('John','Susie')=", does_like("John", "Susie"))
    print("does_like('Susie','John')=", does_like("Susie", "John"))
    print("is_parent('John','Adam') =", is_parent("John", "Adam"))
    print("is_between('A','B','C')  =", is_between("A", "B", "C"))
    print()
    print("Parent(John, ?) ->", children_of("John"))
    print("Parent(?, Susan) ->", parents_of("Susan"))
