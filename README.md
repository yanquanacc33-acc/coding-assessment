# Coding Assessment

## 1. `quiz.py`

Implement the following functions:

```python
def reverse_list(l: list):
    """
    Reverse a list without using any built-in functions.
    The function should return a reversed list.
    Input l is a list that may contain any type of data.
    """
    pass
```

```python
def solve_sudoku(matrix):
    """
    Write a program to solve a 9x9 Sudoku board.
    The board must be completed so that every row, column, and 3x3 section
    contains all digits from 1 to 9.
    Input: a 9x9 matrix representing the board.
    """
    pass
```

## 2. `webapp/main.py`

Build a web service using FastAPI with at least two API endpoints.

### Image Upload And Compression Endpoint

- Allows users to upload an image.
- Provides a compressed version of that image.
- All logic must be implemented within the service itself.
- The compression algorithm does not need to be advanced.
- Compression quality does not matter.
- The API should consider concurrent access.
- Any Python image-processing library may be used.

### Processing History Endpoint

- Returns the history of processed images.
- No database configuration is required.
- All storage must be in-memory only.

### Restrictions

- Do not use external services such as cloud platforms, serverless environments, or third-party SDKs/APIs.
- Do not introduce additional external dependencies unless necessary.
- Consider edge cases, reliability, performance, and readability.

### README Requirement

Include a README file that explains how to review and test the application with test cases.

### Important Notes

- This assignment evaluates design and development skills.
- Make the service robust and reliable.
- Additional features are not required, but may be included if essential.
- Focus on code quality over feature quantity.

## 3. `review.py`

Review and refactor the following five code snippets. Identify issues, explain the problems, and provide corrected versions.

```python
# Review 1
def add_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list
```

```python
# Review 2
def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."
```

```python
# Review 3
class Counter:
    count = 0
    def __init__(self):
        self.count += 1
    def get_count(self):
        return self.count
```

```python
# Review 4
import threading

class SafeCounter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1

def worker(counter):
    for _ in range(1000):
        counter.increment()

counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

```python
# Review 5
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] =+ 1
        else:
            counts[item] = 1
    return counts
```

## 4. `algo.py` Optional

We start with a constructor for a linked list, `cons`, which takes a required argument `head` and an optional argument `tail`. It returns a linked list representation where the first element is `head` and the rest of the elements are contained in the `tail` linked list. Empty lists are represented by `None` in Python.

For example:

```python
cons(1, cons(2, cons(3, cons(4))))
```

This constructs a linked list with four elements: `1 2 3 4`.

The `listToString` method converts the list to a string, where the string representations of each element are joined by a single space.

The `myMap` method takes a unary function `fn` and a linked list `list`. It calls `fn` in order over each element in `list` and returns a linked list of the return values of `fn`.

The `myReduce` method calls a reducer function `fn` from the beginning of the list to the end and returns the result.

For example, if the list is:

```python
cons(1, cons(2, cons(3)))
```

Then:

```python
myReduce(fn, accm, list)
```

should return:

```python
fn(fn(fn(accm, 1), 2), 3)
```

All three methods above are implemented using recursion.

### Implement `myReduceRight`

Implement the `myReduceRight` method. This is similar to `myReduce`, except it calls the reducer function `fn` from the end of the list to the beginning.

For example, if the list is:

```python
cons(1, cons(2, cons(3)))
```

Then:

```python
myReduceRight(fn, accm, list)
```

should return:

```python
fn(1, fn(2, fn(3, accm)))
```

### Requirements

- Implement the solution using recursion instead of explicit `for` or `while` loops.
- Do not use the previously defined `listToString`, `myMap`, or `myReduce` methods.
- Do not mutate the original list.

### Checks

- `myReduceRight(xTimesTwoPlusY, 0, exampleList)` should evaluate to `20`.
- `myReduceRight(unfoldCalculation, "accm", exampleList)` should evaluate to `fn(1, fn(2, fn(3, fn(4, accm))))`.
- `myReduceRight(printXAndReturnY, 0, exampleList)` should print the content of the list in reverse order.

### Starter Code

```python
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
```
