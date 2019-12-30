#dockercompose
FROM ubuntu:18.04

#pull image to build on

RUN apt-get update; apt-get clean \
  && apt-get upgrade \
  && apt-get install -y wget \
  && apt-get install -y gnupg2 \
  && apt-get install -y curl xvfb unzip python3-pip \
  && apt-get install -y fonts-liberation libappindicator3-1 libasound2 \
  && apt-get install -y libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2\
  && apt-get install -y libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
  && apt-get install -y libpangocairo-1.0-0 libxcomposite1 libxcursor1 libxi6 libxrandr2 \
  && apt-get install -y libxrender1 libxtst6 xdg-utils \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update; apt-get clean \
  && apt-get upgrade \
  && apt-get install libxss1 \
  && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN apt-get -y install -f
RUN wget -N https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN chmod +x chromedriver

RUN mv -f chromedriver /usr/local/share/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

#RUN apt install python-pip
RUN pip3 install wheel

WORKDIR /usr/src
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./config /usr/src/config
COPY ./radio_webscraper /usr/src/radio_webscraper
RUN ls 

EXPOSE 8080
CMD ["python3", "/usr/src/radio_webscraper/app.py"]