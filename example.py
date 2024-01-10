## This is an example script, please make sure you updated the .env file with your own credentials,
## and that LM studio has a running server for you to connect to.

from src.__init__ import *

c = client("You are a helpful AI assistant.")
c.chat()
