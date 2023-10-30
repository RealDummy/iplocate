# iplocate

an IP address locator


## setup

First, have an API key for the ipstack api. One can be attained on the [ipstack website](https://ipstack.com/signup/free).
Paste the api key into a file and name it 'apikey.txt'. Install dependencies needed with `pip install -r requirements.txt`.


## usage

To use the tool run `python iplocate.py <ip>` replacing `<ip>` with the IP to look up the location of.
If no IP is given, IPs will be read from stdin, separated by newlines.

The program returns the latitude, longitude pair separated by a space, or - - if there is an error in the input.
If multiple IPs are read in from stdin, they will be printed in the same order they were read in.


## docker

There is a Dockerfile for this project. Building the image works as one would expect, but it must be run with the -it flags.
This is because the tool isn't very useful without you seeing its output,
and sometimes it needs to read stdin, so these flags are needed.


## security

There are a few security risks I considered when writing this tool. The most important and easiest to address is hiding the API key. This is done by not providing one and having the user of the tool have one instead. The other large risk is sending an http request with user input inside it. I don't foresee this being an issue in this program because it only makes the request if the user input converts into an ip address.


## code explanation

The code is pretty simple but I made a few choices when designing the program that I thought are worth pointing out. First is the program can either take an argument or read from stdin (but not both). Often when chaining unix commands it is convenient to pipe the output of one command into the input of another, so accepting input from stdin saves the user an xargs headache. I also made the output extremely simple, so another program can easily use the latitude longitude pairs as input without parsing json or filtering out fluff. I find it's better to have to read the readme or man page once rather than filter out words on every command invocation.

