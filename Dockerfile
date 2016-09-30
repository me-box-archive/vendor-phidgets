FROM debian:jessie

#install phydgets driver
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates wget curl build-essential libusb-dev unzip python python-pip && rm -rf /var/lib/apt/lists/* \
 && wget -O libphidget.tar.gz "http://www.phidgets.com/downloads/libraries/libphidget.tar.gz" \
 && tar -xzvf ./libphidget.tar.gz \
 && cd libphidget* \ 
 && ./configure --disable-jni \
 && make \ 
 && make install

#Python modules
RUN wget -O PhidgetsPython.zip "http://www.phidgets.com/downloads/libraries/PhidgetsPython.zip" \
	&& unzip PhidgetsPython.zip \
	&& cd PhidgetsPython \
	&& python setup.py install

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . .

LABEL databox.type="driver"

EXPOSE 3000

RUN apt-get autoremove -y ca-certificates wget curl build-essential libusb-dev unzip 

CMD ["python","app.py"]