```
openssl req -new -newkey rsa:2048 -nodes -keyout wildcard_nidhinpattaniyil_com.key -out wildcard_nidhinpattaniyil_com.csr
```

values entered
```
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:NY
Locality Name (eg, city) []:New York
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Nidhin
Organizational Unit Name (eg, section) []:website
Common Name (e.g. server FQDN or YOUR name) []:*.nidhinpattaniyil.com
Email Address []:npatta01@gmail.com
```


Merge certificate
```
cat *__nidhin*.crt *__nidhin*.ca-bundle >> wildcard_nidhinpattaniyil_com_cert_chain.crt
remove new line characters
```

Validate Certificate
```
openssl x509 -noout -modulus -in wildcard_nidhinpattaniyil_com_cert_chain.crt | openssl md5
openssl rsa -noout -modulus -in wildcard_nidhinpattaniyil_com.key | openssl md5
openssl req -noout -modulus -in wildcard_nidhinpattaniyil_com.csr | openssl md5
```


Rename certs
```
cp wildcard_nidhinpattaniyil_com.key tls.key
cp wildcard_nidhinpattaniyil_com_cert_chain.crt tls.crt
```

Add SecretMap
```
kubectl create secret generic prod-tls --from-file=tls.key --from-file=tls.crt -n=prod
kubectl create secret generic wildcard-tls --from-file=tls.key --from-file=tls.crt -n=nginx-ingress
```