#!/bin/sh

chown -R app:app .
su-exec app python run.py