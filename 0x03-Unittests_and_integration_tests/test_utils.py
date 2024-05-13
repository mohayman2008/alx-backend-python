#!/usr/bin/env python3
'''This module contains unittest test cases for functions in "utils.py"'''
import unittest

from parameterized import parameterized  # type: ignore
from typing import Any, Mapping, Sequence

from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    '''TestCase for "utils.access_nested_map"'''

    @parameterized.expand([
        ("not maximum depth", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("maximum depth", {"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, name: str,
                               nested_map: Mapping, path: Sequence,
                               expected: Any) -> None:
        '''Testing that function "utils.access_nested_map" returns the
        expected output'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("digging in empty dict", {}, ("a",), "a"),
        ("digging deeper than max-depth", {"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, name: str,
                                         nested_map: Mapping, path: Sequence,
                                         expected_msg) -> None:
        '''Testing that function "utils.access_nested_map" returns the
        expected output'''
        with self.assertRaises(KeyError, msg=expected_msg):
            access_nested_map(nested_map, path)
