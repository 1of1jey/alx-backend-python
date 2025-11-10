#!/usr/bin/env python3
import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path.
    
    Args:
        nested_map: A nested map
        path: A sequence of keys representing a path to the value
        
    Returns:
        The value at the path
        
    Raises:
        KeyError: If the path is invalid
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """Get JSON from a remote URL.
    
    Args:
        url: The URL to fetch
        
    Returns:
        The JSON response as a dictionary
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """Memoize decorator.
    
    Caches the result of a method and returns the cached result
    on subsequent calls.
    
    Args:
        fn: The function to memoize
        
    Returns:
        The decorated function
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        """Memoized wrapper"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
