## Jetson Nano -- experiments and such  

---
# Good alternative info 
* appears to be VERY much like my clone-board
* [Waveshare_wiki](https://www.waveshare.com/wiki/JETSON-NANO-DEV-KIT)
---
* for training
* [Official_nVidia_hub](https://catalog.ngc.nvidia.com/?filters=&orderBy=scoreDESC&query=nano&page=&pageSize=)
* [Jetson_ZOO](https://elinux.org/Jetson_Zoo)

---
* These steps are a backup documenting what I did --
---
# Steps attempting to update Python version above 3.6

## OpenSSL

* cd /opt
* sudo wget https://www.openssl.org/source/openssl-1.1.1q.tar.gz --no-check-certificate
* sudo mkdir /opt/openssl
* sudo tar xfvz openssl-1.1.1q.tar.gz --directory /opt/openssl
* export LD_LIBRARY_PATH=/opt/openssl/lib
* cd /opt/openssl/openssl-1.1.1q/
* sudo ./config --prefix=/opt/openssl --openssldir=/opt/openssl/ssl
* sudo make
* sudo make test
* sudo make install
* sudo ln -s /usr/local/bin/openssl /usr/bin/openssl

## Python 3.9.13

* cd /usr/src 
* sudo wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz 
* sudo tar xzf Python-3.9.13.tgz
* cd /usr/src/Python-3.9.13
* sudo CFLAGS="-I/opt/openssl/include/" LDFLAGS="${LDFLAGS} -Wl,-rpath=$LD_LIBRARY_PATH" ./configure --enable-optimizations --with-openssl=/opt/openssl
* sudo make altinstall -j6
* sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3

## pip3

* sudo ln -s /usr/local/bin/pip3.9 /usr/bin/pip3
* pip3 install --upgrade pip
 
##comment : Perfect, still works with "openssl-1.1.1w" and "Python-3.12.2" in March 2024 Thank you! 
* I am trying with openssl-3.3.1 and python-3.8.9
