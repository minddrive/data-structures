"""
Test suite for the reference linked list implementation.
"""

import pytest

from linked_list.linked_list import Node, LinkedList, LinkedListError


def test_create_node():
    """Create a simple node."""
    test_node = Node('abc')
    assert test_node.data == 'abc'
    assert test_node.prev_node is None
    assert test_node.next_node is None


def test_create_node_no_data():
    """Ensure failure when creating a node with no data."""
    with pytest.raises(TypeError):
        test_node = Node()


def test_create_linked_list():
    """Create a simple linked list (no data)."""
    test_linked_list = LinkedList()
    assert test_linked_list.head is None
    assert test_linked_list.tail is None
    assert test_linked_list.current is None
    assert test_linked_list.length == 0


def test_create_linked_list_with_data():
    """Create a linked list with initial data."""
    test_linked_list = LinkedList(['abc', 'def', 'ghi'])
    assert test_linked_list.head is not None
    assert test_linked_list.head.data == 'abc'
    assert test_linked_list.tail is not None
    assert test_linked_list.tail.data == 'ghi'
    assert test_linked_list.current is not None
    assert test_linked_list.current.data == 'ghi'
    assert test_linked_list.length == 3
    assert test_linked_list.gather_node_data(all_nodes=True) == \
           [(0, 'abc'), (1, 'def'), (2, 'ghi')]
    