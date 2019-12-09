""" AVL Tree implementation. """


class Node:
    """ AVLTree Node.
    Left and Right subtrees, if not exist, is None. """

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class AVLTree:
    """ A balanced AVL Tree implementation.
    Has three properties: balance, height and node. """

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    """ Functions to be used from outside """

    def insert(self, key):
        tree = self.node

        new_node = Node(key)

        if tree is None:
            self.node = new_node
            self.node.left = AVLTree()
            self.node.right = AVLTree()
            # print("Inserted key [" + str(key) + "]")

        elif key < tree.key:
            self.node.left.insert_event(key)

        elif key > tree.key:
            self.node.right.insert_event(key)

        else:
            print("Key [" + str(key) + "] already in tree.")

        self.make_balanced()

    def delete(self, key):
        if self.node is not None:
            if self.node.key == key:
                # print("Deleting ... " + str(key))
                if self.node.left.node is None and self.node.right.node is None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that
                elif self.node.left.node is None:
                    self.node = self.node.right.node
                elif self.node.right.node is None:
                    self.node = self.node.left.node

                # Both children present
                else:
                    replacement = self.successor(self.node)
                    if replacement is not None:  # sanity check
                        # print("Found replacement for " + str(key) + " -> " + str(replacement.key))
                        self.node.key = replacement.key
                        # replaced. Now delete the key from right child
                        self.node.right.delete(replacement.key)
                self.make_balanced()
                return
            elif key < self.node.key:
                self.node.left.delete(key)
            elif key > self.node.key:
                self.node.right.delete(key)

            self.make_balanced()
        else:
            return

    def min(self):
        if self.node is None:
            return None
        else:
            if self.node.left.node is None:
                return self.node.key
            else:
                return self.node.left.get_nearest_event()

    def predecessor(self, node):
        """
        Find the biggest valued node in LEFT child
        """
        node = node.left.node
        if node is not None:
            while node.right is not None:
                if node.right.node is None:
                    return node
                else:
                    node = node.right.node
        return node

    def successor(self, node):
        """
        Find the smallest valued node in RIGHT child
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
        l = self.node.left.inorder()
        for i in l:
            inlist.append(i)

        inlist.append(self.node.key)

        l = self.node.right.inorder()
        for i in l:
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

        self.node = B
        B.right.node = A
        A.left.node = T

    def rotate_left(self):
        # print('Rotating ' + str(self.node.key) + ' left')
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T

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