#!/bin/bash
sudo chown $USER:$USER db.sqlite
export FLASK_ENV=development
flask db upgrade $1
