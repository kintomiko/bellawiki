#!/bin/bash

nohup uwsgi --socket :8630 --module wsgi &
