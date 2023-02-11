#!/bin/bash

set -e

virtualenv --without-pip virtualenv -p /usr/bin/python3.9
pip install supabase --target virtualenv/lib/python3.9/site-packages
