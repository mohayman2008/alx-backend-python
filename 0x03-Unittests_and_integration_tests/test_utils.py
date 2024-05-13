#!/usr/bin/env python3
'''This module contains unittest test cases for functions in "utils.py"'''
from typing import Any, Dict, Tuple
import unittest

# from parameterized import parameterized  # type: ignore
parameterized = __import__("parameterized").parameterized

# from utils import access_nested_map
access_nested_map = __import__("utils").access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    '''TestCase for "utils.access_nested_map"'''

    @parameterized.expand([
        ("not maximum depth", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("maximum depth", {"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, name: str,
                               nested_map: Dict, path: Tuple,
                               expected: Any) -> None:
        '''Testing "utils.access_nested_map" expected output'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("digging in empty dict", {}, ("a",), "a"),
        ("digging deeper than max-depth", {"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, name: str,
                                         nested_map: Dict, path: Tuple,
                                         expected_msg) -> None:
        '''Testing that function "utils.access_nested_map" raises the expected
        exception with the right exception messages'''
        with self.assertRaises(KeyError, msg=expected_msg):
            access_nested_map(nested_map, path)
