#!/bin/bash
export LANG=en_IE.UTF-8
LC_CTYPE="en_IE.UTF-8"
LC_ALL=
./dfa.py $1 | mail  -E  -s "Passport status changed" me@example.com -c cc@example.org

