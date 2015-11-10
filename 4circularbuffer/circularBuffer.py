# Implementation using circular lists

import ctypes


class Node:
    """ Node class used for making node objects """

    def __init__(self, element, nextitem=None):
        self._element = element
        self._next = nextitem

    def __str__(self):
        return str(self._element)

    def next(self, new):
        self._next = new


class dequeArray:
    """Implementation of circular buffer in dynamic array"""

    def __init__(self, inlist=[]):
        self._totalElements = len(inlist)
        self._tail = None
        if self._totalElements == 0:
            self._capacity = 2
        else:
            self._capacity = 2 * self._totalElements
        self._startIndex = self._capacity // 2
        self._allocateBlock = self._makeArray(self._capacity)
        i = self._startIndex
        for item in range(self._totalElements):
            try:
                self._allocateBlock[i] = Node(inlist[item], inlist[item+1])
                i += 1
            except IndexError:
                self._allocateBlock[i] = Node(inlist[item], inlist[0])
                i += 1
        # self._tail = self._allocateBlock[self._totalElements]

    def __len__(self):
        return self._totalElements

    def __getitem__(self, index):
        if not 0 <= index < self._totalElements:
            raise IndexError("Index not in range.")
        return self._allocateBlock[self._startIndex + index]

    def __setitem__(self, key, value):
        if not 0 <= key <= self._totalElements:
            raise IndexError("Index not in range.")
        else:
            self._allocateBlock[self._startIndex + key]._element = value

    def isEmpty(self):
        return self._totalElements == 0

    def append(self, item):
        if self._startIndex + self._totalElements == self._capacity:
            self._resizeArray()

        self._allocateBlock[self._startIndex + self._totalElements] = Node(item, None)     # edit using Node class
        self._totalElements += 1
        # print("Toatal elements: ", self._totalElements)
        self._allocateBlock[(self._startIndex + self._totalElements) - 1]._next = self._allocateBlock[self._startIndex]
        self._allocateBlock[(self._startIndex + self._totalElements) - 2]._next = self._allocateBlock[(self._startIndex + self._totalElements) - 1]
        self._tail = self._allocateBlock[(self._startIndex + self._totalElements) - 1]

    def preappend(self, item):
        if self._startIndex == 0:
            self._resizeArray()

        self._startIndex -= 1
        self._allocateBlock[self._startIndex] = Node(item, None)
        self._allocateBlock[self._startIndex]._next = self._allocateBlock[self._startIndex + 1]
        self._allocateBlock[(self._startIndex + self._totalElements) - 1]._next = self._allocateBlock[self._startIndex]
        self._totalElements += 1

    def removeFirst(self):
        item = self._allocateBlock[self._startIndex]
        # self._allocateBlock[self._startIndex] = None
        for i in range(self._totalElements):
            self._allocateBlock[self._startIndex + i] = self._allocateBlock[self._startIndex + i + 1]
            if i == (self._totalElements - 1):
                self._allocateBlock[self._startIndex + i]._next = self._allocateBlock[self._startIndex]
                continue
            self._allocateBlock[self._startIndex + i]._next = self._allocateBlock[self._startIndex + i + 2]

        self._allocateBlock[self._startIndex + self._totalElements] = None
        self._totalElements -= 1
        return item

    def removeLast(self):
        item = self._allocateBlock[self._startIndex + self._totalElements]
        self._allocateBlock[self._startIndex + self._totalElements] = None
        self._totalElements -= 1
        self._allocateBlock[self._startIndex + self._totalElements]._next = self._allocateBlock[self._startIndex]
        return item

    def insert(self, index, item):
        if not 0 <= index < self._totalElements:
            raise IndexError("Index out of range")

        if self._startIndex + self._totalElements == self._capacity:
            self._resizeArray()

        for i in range(self._totalElements, index, -1):
            self._allocateBlock[self._startIndex + i]._element = self._allocateBlock[self._startIndex + i - 1]._element
            if i == self._totalElements:
                self._allocateBlock[self._startIndex + i]._next = self._allocateBlock[self._startIndex]
                continue
            self._allocateBlock[self._startIndex + i]._next = self._allocateBlock[self._startIndex + i + 1]

        self._allocateBlock[self._startIndex + index]._element = item

        self._allocateBlock[self._startIndex + index]._next = self._allocateBlock[self._startIndex + index + 1]
        self._allocateBlock[self._startIndex + index - 1]._next = self._allocateBlock[self._startIndex + index]
        self._totalElements += 1

    def remove(self, index):
        if not 0 <= index < self._totalElements:
            raise IndexError("Index not in range")
        item = self._allocateBlock[self._startIndex + index]
        for i in range(index, self._totalElements - 1):
            self._allocateBlock[self._startIndex + i] = self._allocateBlock[self._startIndex + i + 1]
        self._allocateBlock[self._startIndex + index - 1]._next = self._allocateBlock[self._startIndex + index]
        self._allocateBlock[self._startIndex + self._totalElements] = None
        self._totalElements -= 1
        return item

    def __str__(self):
        """overloading built in print function. """
        string = " "
        for i in range(self._totalElements):
            string += str(self.__getitem__(i))
            if i != (self._totalElements-1):
                string += ", "
        return string + "."

    def _resizeArray(self):
        newCapacity = 2 * self._capacity
        newArray = self._makeArray(newCapacity)
        newStartIndex = self._totalElements
        for item in range(self._totalElements):
            newArray[newStartIndex + item] = self._allocateBlock[newStartIndex + item]
        self._allocateBlock = newArray
        self._capacity = newCapacity
        self._startIndex = newStartIndex

    def _makeArray(self, capacity):
        """Uses cytpes for returning low level arrays."""
        return (capacity * ctypes.py_object)()


def main():
    d = dequeArray([0, 1, 2, 3, 4])
    print("Is the array empty : ", d.isEmpty())
    print()

    print("Length of the array is : ", len(d))
    print()

    print("Item at index 2 is :", d[2])
    print()

    print("Capacity is: ", d._capacity)     # remove this after testing
    print()

    print("Setting item at index 2 to be 3")
    print("Prior to change: ", d[2])
    d[2] = 3
    print("Changing---")
    print("The value at index 2 after change is: ", d[2])
    print()
    print()
    print("All elements in the array: ", d[3], d[2], d[1], d[0])
    print("All elements in the array: ", d[3]._next, d[2]._next, d[1]._next, d[0]._next)

    print("Capacity is: ", d._capacity)     # remove this after testing
    print()

    print("Appending object at the end...")
    print()
    d.append(5)
    print("New length of the array is: ", len(d))
    print("Element at the last index is:", d[5])
    print("All elements in the array: ", d[3], d[2], d[1], d[0])
    print("All elements in the array: ", d[3]._next, d[2]._next, d[1]._next, d[0]._next)

    print()

    print("Preappend test")
    print("preappending value 7")
    d.preappend(7)
    print("Value at index 0 is :", d[0])
    print("All elements in the array: ", d[3], d[2], d[1], d[0])
    print("All elements in the array: ", d[3]._next, d[2]._next, d[1]._next, d[0]._next)

    print()

    print("Remove First item test")
    print("Value at first index: ", d[0])
    d.removeFirst()
    print("[after method applied] Value at first index: ", d[0])
    print("All elements in the array: ", d[3], d[2], d[1], d[0])
    print("All elements in the array: ", d[3]._next, d[2]._next, d[1]._next, d[0]._next)

    print()
    print("Remove Last item test")
    print("Value at last index: ", d[4])
    d.removeFirst()
    print("[after method applied] Value at last index: ", d[3])
    print("All elements in the array: ", d[3], d[2], d[1], d[0])
            # value of d[1] was changed earlier in the main funciton
    print("All elements in the array: ", d[3]._next, d[2]._next, d[1]._next, d[0]._next)

    print()

    print("Testing insert method")
    print("Inserting value 2 at d[1]")
    print("Value at d[1] before insert: ", d[1])
    d.insert(1, 2)
    print("Value at d[1] after insert: ", d[1])
    print("All elements in the array: ", d[3], d[2], d[1], d[0])
    print("All elements in the array: ", d[3]._next, d[2]._next, d[1]._next, d[0]._next)

    print()

    print("Testing remove method")
    print("Removing value at d[2]")
    print("Value at d[2] before remove: ", d[2])
    d.remove(2)
    print("Value at d[2] after remove: ", d[2])
    print("All elements in the array: ", d[3], d[2], d[1], d[0])
    print("All elements in the array: ", d[3]._next, d[2]._next, d[1]._next, d[0]._next)

    print()
    print("Testing print function")
    print(d)    # prints the list after removing and inserting items i.e. prints an edited array


if __name__ == '__main__':
    main()