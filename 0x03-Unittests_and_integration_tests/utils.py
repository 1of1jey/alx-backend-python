#!/usr/bin/env python3
import requests

def get_json(url):
    response = requests.get(url)
    return response.json()
