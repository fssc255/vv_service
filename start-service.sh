#!/bin/bash

cd src && uv run gunicorn -w 4 -b 127.0.0.1:6590 app:app