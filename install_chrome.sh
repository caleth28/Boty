#!/bin/bash
apt-get update && apt-get install -y wget unzip
wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /tmp/chrome.deb || apt-get -fy install
rm /tmp/chrome.deb

wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip -d /usr/local/bin/
rm /tmp/chromedriver.zip
