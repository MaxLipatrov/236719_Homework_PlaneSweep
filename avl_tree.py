""" AVL Tree implementation. """
from typing import Optional


class Node:
    """ AVLTree Node.
    Left and Right subtrees, if not exist, is None. """

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class AVLTree:
    """ A balanced AVL Tree implementation.
    Has three properties: balance, height and node. """

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    """ Functions to be used from outside """

    def insert(self, key, parent=None) -> bool:
        tree = self.node
        if tree is None:
            new_node = Node(key)
            self.node = new_node
            self.node.left = AVLTree()
            self.node.right = AVLTree()
            # print("Inserted key [" + str(key) + "]")
            if parent:
                self.node.parent = parent
            res = True

        elif key < tree.key:
            res = self.node.left.insert(key, self.node)

        elif key > tree.key:
            res = self.node.right.insert(key, self.node)

        else:
            # print("Key [" + str(key) + "] already in tree.")
            res = False

        self.make_balanced()
        return res

    def delete(self, key) -> bool:
        res = False
        if self.node is not None:
            if self.node.key == key:
                # print("Deleting ... " + str(key))
                if self.node.left.node is None and self.node.right.node is None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that
                elif self.node.left.node is None:
                    parent = self.node.parent
                    self.node = self.node.right.node
                    self.node.parent = parent
                elif self.node.right.node is None:
                    parent = self.node.parent
                    self.node = self.node.left.node
                    self.node.parent = parent
                else:
                    # Both children present
                    replacement = self.successor(self.node)
                    if replacement is not None:  # sanity check
                        # print("Found replacement for " + str(key) + " -> " + str(replacement.key))
                        self.node.key = replacement.key
                        # replaced. Now delete the key from right child
                        self.node.right.delete(replacement.key)
                self.make_balanced()
                return True
            elif key < self.node.key:
                res = self.node.left.delete(key)
            elif key > self.node.key:
                res = self.node.right.delete(key)

            self.make_balanced()
            return res
        else:
            # No one node to delete
            return False

    def min(self):
        """ Returns a smallest one key in a tree. """
        if self.node is None:
            return None
        else:
            if self.node.left.node is None:
                return self.node.key
            else:
                return self.node.left.min()

    def find(self, key) -> Optional[Node]:
        """ Returns a node of current key, if exist, None otherwise. """
        if self.node is None:
            return None
        else:
            if self.node.key == key:
                return self.node
            elif key < self.node.key:
                return self.node.left.find(key)
            else:
                return self.node.right.find(key)

    def predecessor(self, current_node) -> Optional[Node]:
        """
        Returns the predecessor of a given node - max in left subtree.
        If left subtree is empty, predecessor is a parent.
        If there's no parent - there's no predecessor.
        """
        node = current_node.left.node
        if node is not None:
            while node.right is not None:
                if node.right.node is None:
                    return node
                else:
                    node = node.right.node
        else:
            # Left subtree is empty
            if current_node.parent is not None:
                if current_node.parent.right.node == current_node:
                    return current_node.parent
        return None

    def successor(self, node) -> Optional[Node]:
        """
        Returns the successor node of a given node - min in right subtree
        """
        node = node.right.node
        if node is not None:  # just a sanity check

            while node.left is not None:
                # print("LS: traversing: " + str(node.key))
                if node.left.node is None:
                    return node
                else:
                    node = node.left.node
        return node

    def inorder(self):
        if self.node is None:
            return []

        inlist = []
        inorder = self.node.left.inorder()
        for i in inorder:
            inlist.append(i)

        inlist.append(self.node.key)

        inorder = self.node.right.inorder()
        for i in inorder:
            inlist.append(i)

        return inlist

    """ Internal functions """

    def is_balanced(self):
        if self.node is None:
            return True

        # We always need to make sure we are balanced
        self.update_heights()
        self.update_balances()
        return (abs(self.balance) < 2) and self.node.left.is_balanced() and self.node.right.is_balanced()

    def make_balanced(self):
        """
        Rebalance a particular (sub)tree
        """
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()  # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rotate_right()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()  # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.rotate_left()
                self.update_heights()
                self.update_balances()

    def rotate_right(self):
        # print('Rotating ' + str(self.node.key) + ' right')
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self_parent = self.node.parent

        self.node = B
        B.right.node = A
        A.left.node = T

        self.node.parent = self_parent
        if B.right.node is not None:
            B.right.node.parent = self.node
        if A.left.node is not None:
            A.left.node.parent = A

    def rotate_left(self):
        # print('Rotating ' + str(self.node.key) + ' left')
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self_parent = self.node.parent

        self.node = B
        B.left.node = A
        A.right.node = T

        self.node.parent = self_parent
        if B.left.node is not None:
            B.left.node.parent = self.node
        if A.right.node is not None:
            A.right.node.parent = A

    def update_heights(self, recurse=True):
        if self.node is not None:
            if recurse:
                if self.node.left is not None:
                    self.node.left.update_heights()
                if self.node.right is not None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if self.node is not None:
            if recurse:
                if self.node.left is not None:
                    self.node.left.update_balances()
                if self.node.right is not None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0
