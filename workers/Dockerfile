FROM --platform=linux/amd64 python:3.11.6-bookworm

WORKDIR /workers
RUN apt update

# Install firefox TODO replace with modern version?
ENV FIREFOX_SETUP=firefox-setup.tar.bz2
RUN apt-get purge firefox
RUN wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/  && \
    ln -s /opt/firefox/firefox /usr/bin/firefox  && \
    rm $FIREFOX_SETUP

RUN echo "GECKODRIVER_VERSION="$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")') > /tmp/geckodriver_version
RUN export $(cat /tmp/geckodriver_version) && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    rm /tmp/geckodriver_version

# TODO Any of this needed?
RUN apt install --no-install-recommends -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 \
    xvfb 

RUN pip install --upgrade pip poetry
COPY ./pyproject.toml /workers/
COPY ./README.md /workers/README.md

RUN poetry install --no-root

# set display port to avoid crash. TODO Needed?
ENV DISPLAY=:99
