#!/bin/bash

docker run --rm -it -p 443:443 -v $(pwd):/app/serve ranger11danger/secure_serve || docker run --rm -it -p 443:443 -v $(pwd):/app/serve secure_serve
