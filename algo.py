'''
We start with a constructor for a linked list, cons, which takes a required argument head and an optional argument tail. It returns a linked list representation where the first element is head and the rest of the elements are contained in the tail linked list. Empty lists are represented by None in Python.
 
For example, cons(1, cons(2, cons(3, cons(4)))) constructs a linked list with 4 elements, 1 2 3 4.
 To make it easy to inspect the content of a linked list, the listToString method is defined to convert the list to a string, where the string representations of each element are joined by a single space in between.
 The myMap method takes a unary function fn and a linked list list. It calls fn in order over each element in list and returns a linked list of the return values of fn.
 The myReduce method calls a reducer function fn from the beginning of the list to the end and returns the result. For example, if the list is cons(1, cons(2, cons(3))), myReduce(fn, accm, list) should return the result of evaluating fn(fn(fn(accm, 1), 2), 3).
 All three methods above are implemented using recursion, leveraging the recursive structure of the linked list.
 Implementing myReduceRight
 Implement the myReduceRight method. This is similar to myReduce, with the difference that it calls the reducer function fn from the end of the list to the beginning. For example, if the list is cons(1, cons(2, cons(3))), myReduceRight(fn, accm, list) should return the result of evaluating fn(1, fn(2, fn(3, accm))).
 Requirements:
You SHOULD implement your solution using recursion, instead of anyexplicit for / while loops.
You MUST NOT use any of the previously defined listToString, myMap, myReduce methods in your implementation.
You MUST NOT mutate the original list.
 
To check your implementation, verify that:
l  myReduceRight(xTimesTwoPlusY, 0, exampleList) should evaluate to 20.

l  myReduceRight(unfoldCalculation, "accm", exampleList) should evaluate to fn(1, fn(2, fn(3, fn(4, accm)))).

l  myReduceRight(printXAndReturnY, 0, exampleList) should print out the content of the list in the reverse order.
'''
class LinkedList:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

def cons(head, tail=None):
    return LinkedList(head, tail)

def listToString(list):
    if list is None:
        return ""
    if list.tail is None:
        return str(list.head)
    return str(list.head) + " " + listToString(list.tail)

def myMap(fn, list):
    if list is None:
        return None
    return cons(fn(list.head), myMap(fn, list.tail))

def myReduce(fn, accm, list):
    if list is None:
        return accm
    return myReduce(fn, fn(accm, list.head), list.tail)
# Implement myReduceRight
def myReduceRight(fn, accm, list):
    if list is None:
        return accm
    return fn(list.head, myReduceRight(fn, accm, list.tail))

def xTimesTwoPlusY(x, y):
    return x * 2 + y

def unfoldCalculation(x, y):
    return f"fn({x}, {y})"

def printXAndReturnY(x, y):
    print(x)
    return y

exampleList = cons(1, cons(2, cons(3, cons(4))))
print(myReduceRight(xTimesTwoPlusY, 0, exampleList))
print(myReduceRight(unfoldCalculation, "accm", exampleList))
myReduceRight(printXAndReturnY, 0, exampleList)
