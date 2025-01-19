# nationstates-endorsement-checker
A simple python script to get a list of nations to endorse in NationStates.net

It also includes a [simple progress bar](https://stackoverflow.com/a/34325723), time tacken and a simple html generator with a button to open all the nation links (with a time delay of 500ms)

Help:
```
usage: nationstates-endorsement-checker.py [-h] [-e NATION [NATION ...]] [-d DELAY] nation

Utility to return a list of nations to endorse

positional arguments:
  nation                Your nation

options:
  -h, --help            show this help message and exit
  -e NATION [NATION ...], --exclude NATION [NATION ...]
                        List of excluded nation
  -d DELAY, --delay DELAY
                        set delay for opening links in html in miliseconds (default: 500)
```
For example to check which nation Testlandia can endorse, but you want to exclude Test Nation and Testlandia2, you run the following command:
```
./nationstates-endorsement-checker.py Testlandia --exclude "Test Nation" Testlandia2
```
In the same folder, there is also the file `to_endorse_nation.html`. This file contains the links of the nations with a button to open all of them with a time delay (to prevent rate limiting). 
