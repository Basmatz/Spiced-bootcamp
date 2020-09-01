#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 13:42:53 2020

@author: stazhe
"""


import slack
import pyjokes
import time

oauth_token = "xoxb-1227345553298-1312086130423-uuolDU1nITg4LILI5FlHQIDN"

client = slack.WebClient(token=oauth_token)

while True:
    joke = pyjokes.get_joke()
    response = client.chat_postMessage(channel='#random', text=f"Here is a Python joke: {joke}")
    time.sleep(10)
