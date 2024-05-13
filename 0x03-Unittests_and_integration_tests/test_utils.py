#!/usr/bin/env python3
'''This module contains unittest test cases for functions in "utils.py"'''
from typing import Any, Mapping, Sequence
import unittest
from unittest.mock import patch

from parameterized import parameterized  # type: ignore
from requests import Response

from utils import *


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


class MockResponse():
    '''Class to mock the Response() object returned by requests.get(url)'''

    def __init__(self, expected_payload=None, *args, **kwargs):
        self.expected_payload = expected_payload

    def json(self):
        '''Mock of the json() method to return the "expected_payload"
        as the object represented by the received JSON'''
        return self.expected_payload


class TestGetJson(unittest.TestCase):
    '''TestCase for "utils.get_json"'''

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url: str, expected_payload: Mapping) -> None:
        '''Testing that function "utils.get_json" returns the expected result
        '''
        with patch("utils.requests.get",
                   return_value=MockResponse(expected_payload)) as mock:
            self.assertEqual(get_json(url), expected_payload)
        mock.assert_called_once()


class TestMemoize(unittest.TestCase):
    '''TestCase for "utils.memoize"'''

    def test_memoize(self) -> None:
        '''Testing that function "utils.memoize" functions as it's supposed to
        '''
        class TestClass:
            '''Test class'''
            def a_method(self) -> int:
                '''Dummy method'''
                return 42

            @memoize
            def a_property(self) -> int:
                '''Memoized property'''
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock:
            test_obj = TestClass()
            self.assertEqual(test_obj.a_property, 42)
            self.assertEqual(test_obj.a_property, 42)
        mock.assert_called_once()
