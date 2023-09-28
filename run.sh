#!/bin/bash

docker run --rm -it -p 443:443 -v $(pwd):/app/serve secure_serve
