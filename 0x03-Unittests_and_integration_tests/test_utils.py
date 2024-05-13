#!/usr/bin/env python3
'''This module contains unittest test cases for functions in "utils.py"'''
from typing import Any, Mapping, Sequence
import unittest

from parameterized import parameterized  # type: ignore

from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    '''TestCase for "utils.access_nested_map"'''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence,
                               expected: Any) -> None:
        '''Testing that function "utils.access_nested_map" returns the
        expected output'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Mapping, path: Sequence,
                                         expected_msg) -> None:
        '''Testing that function "utils.access_nested_map" raises the expected
        exception with the right exception messages'''
        with self.assertRaises(KeyError, msg=expected_msg):
            access_nested_map(nested_map, path)
