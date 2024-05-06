This directory stores private key and public key as files "jwt-private.pem" and "jwt-public.pem"

To generate private key you can use:
````
openssl genrsa -out app/auth/certs/jwt-private.pem 2048
````
To generate public key depends on created private key you can use:
````
openssl rsa -in app/auth/certs/jwt-private.pem -outform PEM -pubout -out app/auth/certs/jwt-public.pem
````
