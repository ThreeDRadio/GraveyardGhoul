#!/bin/bash
cd /usr/local/bin/GraveyardGhoul
source env/bin/activate
python Ghoul.py >> ghoul.log 2&>1
