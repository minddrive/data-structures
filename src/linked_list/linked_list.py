"""
Implementation of a doubly-linked list in Python without using the standard
available list structure Python offers.
"""

from typing import Optional, Sequence


class LinkedListError(Exception):
    """Custom error for LinkedList class."""


class Node:
    """Basic structure for a node in a linked list.

    Currently only supports strings for the data contained in the node;
    this may be expanded later.

    :param data: A string containing text for the node.
    :type data: str
    :param prev_node: The node, if any, that comes before this node.
    :type prev_node: Node
    :param next_node: The node, if any, that comes after this node.
    :type next_node: Node
    """

    def __init__(self, data: str) -> None:
        """Populate node with given data and prepare previous
        and next node attributes.

        :param data: A string containing text for the node.
        :type data: str
        """

        self.data: str = data
        self.prev_node: Optional[Node] = None
        self.next_node: Optional[Node] = None


class LinkedList:
    """Implementation of a doubly-linked list.

    The implementation avoids the use of Python's own list type, in order
    to simulate an implementation that would be found in a language like C.

    :param head: The first node of the linked list.
    :type head: Node, optional
    :param tail: The last node of the linked list.
    :type tail: Node, optional
    :param current: The node currently indexed in the list.
    :type current: Node, optional
    :param length: The number of nodes in the list.
    :type length: int
    """

    def __init__(self, initial_data: Optional[list[str]] = None) -> None:
        """Set up linked list and optionally populate with an initial
        set of data.

        :param initial_data: Optional initial data to populate the list.
        :type initial_data: list[str], optional
        """

        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.current: Optional[Node] = None
        self.length: int = 0

        if initial_data:
            for index, data in enumerate(initial_data):
                if index == 0:
                    self.insert_node(data)
                else:
                    self.insert_node(data, after=True, index=index-1)

    @property
    def at_head(self):
        """Determine if current node is first node."""

        return self.current is self.head

    @property
    def at_tail(self):
        """Determine if current node is last node."""

        return self.current is self.tail

    def set_current_index(self, index: int = 0) -> None:
        """Set the current node to the requested index in the linked list.

        :param index: The position of the desired node in the linked list.
        :type index: int
        :raises LinkedListError: Raised if index is out of bounds or if there
            is an invalid node in the list.
        """

        # TODO: Use the current index to move relative to it, along with
        #       also handling negative indexes.

        if index != 0 and index > self.length - 1:
            raise LinkedListError('Index is out of bounds')

        self.current = self.head
        for _idx in range(index):
            try:
                self.current = self.current.next_node
            except AttributeError as exc:
                raise LinkedListError('Invalid node was reached') from exc

    def insert_node(
        self, data: str, after: bool = False, index: int = 0
    ) -> Node:
        """Create a new node with the given data and insert it into the
        linked list.

        The 'after' parameter controls whether the new node is inserted
        before or after the current node.

        :param data: A string containing text for the new node.
        :type data: str
        :param after: Determine whether the new node is inserted after the
            current node.
        :type after: bool
        :param index: The position of the current node in the linked list.
        :type index:  int
        :return: The new node.
        :rtype: Node
        """

        new_node = Node(data)
        self.set_current_index(index)

        if not self.length:
            self.head = self.tail = new_node
        elif after:
            new_node.prev_node = self.current
            new_node.next_node = self.current.next_node

            if self.at_tail:
                self.tail = new_node
            else:
                self.current.next_node.prev_node = new_node

            self.current.next_node = new_node
        else:
            new_node.prev_node = self.current.prev_node
            new_node.next_node = self.current

            if self.at_head:
                self.head = new_node
            else:
                self.current.prev_node.next_node = new_node

            self.current.prev_node = new_node

        self.current = new_node
        self.length += 1

        return new_node

    def modify_node(self, new_data: str, index: int = 0) -> Node:
        """Update the data for the node at the given index.

        :param new_data: Data to replace current data in the node.
        :type new_data: str
        :param index:  The position of the desired node in the linked list.
        :type index: int
        :return: The modified node.
        :rtype: Node
        """

        self.set_current_index(index)
        self.current.data = new_data

        return self.current

    def remove_node(self, index: int = 0) -> str:
        """Remove the node at the given index.

        Make the next node the current node, and return the data from
        the deleted node.

        :param index: The position of the desired node in the linked list.
        :type index: int
        :return: The data from the deleted node.
        :rtype: str
        """

        self.set_current_index(index)

        if self.current.prev_node is not None:
            self.current.prev_node.next_node = self.current.next_node
        if self.current.next_node is not None:
            self.current.next_node.prev_node = self.current.prev_node

        node_data = self.current.data[:]  # String is copied to avoid ref
        node_to_delete = self.current
        self.current = self.current.next_node
        self.length -= 1
        del node_to_delete

        return node_data

    def previous_node(self) -> Node:
        """Move to the previous node in the list from the current node.

        If at the beginning of the list, simply return the current node.

        :return: The previous node.
        :rtype: Node
        """

        if self.current.prev_node is not None:
            self.current = self.current.prev_node

        return self.current

    def next_node(self) -> Node:
        """Move to the next node in the list from the current node.

        If at the end of the list, simply return the current node.

        :return: The next node.
        :rtype: Node
        """

        if self.current.next_node is not None:
            self.current = self.current.next_node

        return self.current

    def find_node_by_index(self, index: int = 0) -> Node:
        """Find a specific node at the location of the given index.

        Raise an error if the index passed is out of bounds, otherwise
        return the found node.

        :param index: The position of the desired node in the linked list.
        :type index: int
        :raises LinkedListError: Raised if the index is out of bounds.
        :return: The found node.
        :rtype: Node
        """

        self.current = self.head
        for _idx in range(index):
            try:
                self.current = self.current.next_node
            except AttributeError as exc:
                raise LinkedListError('Index is out of bounds') from exc

        return self.current

    def find_node_by_data(self, data: str) -> Node:
        """Find a specific node from the given data.

        This function will return the first node that has matching data,
        or raise an error if no node is found.

        :param data: The data to search for in the nodes in the linked list.
        :type data: str
        :raises LinkedListError: Raised if no node with the request data
            is found.
        :return: The found node.
        :rtype: Node
        """

        self.current = self.head
        while self.current is not None:
            if self.current.data == data:
                break

            self.current = self.current.next_node
        else:
            raise LinkedListError('No node with given data was found')

        return self.current

    def gather_node_data(
        self, indexes: Optional[Sequence[int]] = None, all_nodes: bool = False
    ) -> list[tuple[int, str]]:
        """Gather the data for each requested node.

        A sequence of indexes may be passed, or 'all_nodes' may be set to
        True to gather the data from all the nodes in the linked list.

        Note that 'all_nodes' will always override any individual indexes
        that may be passed, and any invalid indexes will currently be
        ignored.

        :param indexes: A sequence of indexes for the requested nodes.
        :type indexes: Sequence[int], optional
        :param all_nodes: Determine whether to display data from all
            the nodes.
        :type all_nodes: bool
        """

        if indexes is None:
            indexes = []

        self.current = self.head
        index = 0
        list_data = []

        # TODO: verify the indexes passed are all valid or raise an exception
        while self.current is not None:
            if all_nodes or index in indexes:
                list_data.append((index, self.current.data))
                self.current = self.current.next_node

            index += 1

        return list_data

    def display_nodes(
        self, indexes: Optional[Sequence[int]] = None, all_nodes: bool = False
    ) -> None:
        """Display the data for each requested node.

        A sequence of indexes may be passed, or 'all_nodes' may be set to
        True to print the data from all the nodes in the linked list.

        Note that 'all_nodes' will always override any individual indexes
        that may be passed, and any invalid indexes will currently be
        ignored.

        :param indexes: A sequence of indexes for the requested nodes.
        :type indexes: Sequence[int], optional
        :param all_nodes: Determine whether to display data from all
            the nodes.
        :type all_nodes: bool
        """

        for index, data in self.gather_node_data(indexes, all_nodes):
            print(f'Node {index}: {self.current.data}')
