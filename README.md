# iplocate:

an IP address locator

## setup

First, have an API key for the ipstack api. One can be attained on the [ipstack website](https://ipstack.com/signup/free).
Paste the api key into a file and name it 'apikey.txt'. Install dependancies needed with `pip install -r requirements.txt`.

## usage

To use the tool run `python iplocate.py <ip>` replacing `<ip>` with the IP to look up the location of. 
If no IP is given, IPs will be read from stdin, seperated by newlines.

The program returns the latitude longitude pair seperated by a space, or - - if there is an error in the input. 
If multiple IPs are read in from stdin, they will be printed in the same order they were read in.

## docker

There is a Dockerfile for this project. Building the image works as one would expect, but it must be run with the -it flags.
This is because the tool isnt very useful without you seeing its output, 
and sometimes it needs to read stdin, so these flags are needed.

