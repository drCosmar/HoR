# Dr.Cosmar's "How Of Representatives"

## Congress API & LM Studio Wrapper
A simple script that provides a convenient wrapper for making requests to the [Congress API](https://api.congress.gov/v2/) and interacting with the interface of [LM Studio](https://lmstudio.ai). This tool can be used as part of larger programs or run independently, allowing you to build upon its functionality.

### Prerequisites
- Python 3.11+
- LM Studio ([sign up here](https://www.lmstudio.ai/))

### Installation
1. Run `pip install -r requirements.txt`
2. Add your Congress API key to the .env file.
3. Set up a server using LM Studio.
4. Enter your server information from LM Studio into the .env file.

### Usage
To see an example of how to use this tool, take a look at `example.py`. This file demonstrates the chat function. The `cong.py` module contains all the Congress API calls. For optimal performance, it's recommended to store and sort retrieved data in JSON files rather than making repeated API calls.

### Variables
Leave variables like `DEFAULT` as-is unless you have a specific reason for changing them. Modifying these values may result in your Congress API access being revoked or other unexpected issues.