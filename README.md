# secure-web-transfer
this is docker image that i created in order to do secure transfers over the secure-web-transfer
this container spins up a https sever on `443` that is hosting a file on a random path

## Installing the docker image

to install the docker image you can either run `docker build -t secure_serve .`
or `docker pull ranger11danger/secure_serve`

## Running the Server
after you have built the image you can run it by running `./run.sh`
this will kick of the container and mount your current directory into the containers `/app/serve` folder **so whatever files you want to be able to serve need to be in your current directory**

when you run the image it will spit out a random path like so:
`Initial random path is: /LjkKCy74ub/`
this is the path that the file will be hosted on, you can change this path by running the `set_path <path>` command **NOTE: this path needs to start with a leading `/`**

## Select File to Server
once you have you path set or if you're just going to use the random one, go ahead and run the`choose_file` command this will prompt you to pick which file you want to serve like so:

```bash
1. file1
2. file2
3. file3
Choose a file by number: 
```
whatever number you pick will be the file served

## Start the Server
once you have the file picked run the `start` command and this will generate fresh `certs` and kick off the web app.

now if you navigate to `https://<ip>/<random path>` and accept the self signed cert you will download the file you selected to serve

if you would like to `curl` this file instead just make sure you use the `-k` flag to ignore self signed cert
`curl -k https://<ip>/<random path> -o out` will save the selected file as `out`


## Stop the Server
to stop the server run the `stop` command

## More Encryption

if you would like to make this even more secure you can gpg encrypt the file that you want to serve and then decrypt it on the downloaded side

consider this example for a file we want to encrypt named `testfile`
### GPG Encrypt
to encrypt run `gpg --batch --yes --passphrase "password" --symmetric --cipher-algo AES256 testfile`

this will create and encrypted file named `testfile.gpg`
this will be the file that you want to serve with the web app

### GPG Decrypt
once you have downloaded the encrypted file and need to decrypt it run the following command
`gpg --batch --yes --passphrase "password" --decrypt testfile.gpg > testfile`


and thats it you have now transfered a gpg encrypted file via the https server

