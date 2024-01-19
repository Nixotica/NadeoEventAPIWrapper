# Nadeo Event API Wrapper

## Setup

1. Install python 3.10+ 
2. Set an environment variable "UBI_AUTH" with "Basic <user:pass>" where user:pass is converted to base 64
3. Set an environment variable "MY_CLUB" with the club you want your events to go.
3. Run pip install "git+https://github.com/Nixotica/NadeoEventAPIWrapper.git@release#egg=nadeo_event_api&subdirectory=nadeo_event_api"
4. From /NadeoEventAPIWrapper/ run python3 path/to/script.py

## Development

If you want to contribute to either the premade events (like NCSA Solo League) you can feel free to add them however you want, just make sure to test it locally. 

Make sure to add some tests to new code in nadeo_event_api, and pytest from /NadeoEventAPIWrapper/nadeo_event_api/. It won't run integration tests by default, since it's very easy to hit the API limit and get locked out for a few hours. Only run individual integration tests if you're working on one. 

## Fork

There is a GitHub Action which requires UBI_AUTH and MY_CLUB to be set as secrets to pass. Do the following so the action will pass in your repo:

1. Go to Settings -> Secrets and Variables -> Actions -> New repository secret 
2. In Name put UBI_AUTH and in Secret put the same value as your environment variable UBI_AUTH from Setup step 2.
3. Do this again but for MY_CLUB environment variable. 

## Contact

This is entirely owned by Nick Walters (nixotica@gmail.com) and does not guarantee any functionality to remain unbroken. Reach out if you have any concerns or issues with setup. 