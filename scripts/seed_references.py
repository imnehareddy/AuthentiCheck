#!/usr/bin/env python3
import os
import requests

BASE_URL = 'http://127.0.0.1:5000'

def seed():
    resp = requests.post(f'{BASE_URL}/api/reference/seed')
    print(resp.status_code, resp.text)

if __name__ == '__main__':
    seed()
