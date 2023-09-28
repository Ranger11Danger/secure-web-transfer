FROM python:3.9-slim

# Install openssl for certificate generation
RUN apt-get update && apt-get install -y openssl && apt-get clean

# Install necessary Python packages
RUN pip install flask cmd2

# Copy the necessary files
COPY server.py /app/

WORKDIR /app
RUN mkdir /app/serve

# Script to run at container startup
CMD ["python", "server.py"]
