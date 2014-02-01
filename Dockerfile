###############################################
# Dockerfile for the perfectgift tornado app. #
# Based on ubuntu 13.04                       #
###############################################

FROM ubuntu:13.04
MAINTAINER cyphar <cyphar@cyphar.com>

##################
# Update server. #
##################

# Make sure the repos and packages are up to date
RUN apt-get update
RUN apt-get upgrade -y

############################################
# Install perfectgift server dependencies. #
############################################

# Install python3.
RUN apt-get install -y python3

# Install pillow's dependencies.
RUN apt-get install -y git python3-dev python3-setuptools libjpeg8 zlib1g libtiff4 libfreetype6 liblcms2-2 libwebp4

# Pull, build and install pillow from the git repo.
RUN rm -rf /tmp/pillow-install && mkdir -p /tmp/pillow-install
RUN git clone git://github.com/python-imaging/Pillow.git /tmp/pillow-install
RUN cd /tmp/pillow-install && python3 setup.py install

###################$######################
# Install and configure perfectgift app. #
####################$#####################

# Set up perfectgift server directory.
RUN mkdir -p /srv/perfectgift
WORKDIR /srv/perfectgift

# Copy over the perfectgift app source.
ADD . /srv/perfectgift

# Initialise the sqlite database.
RUN python3 db/initdb.py

# Set up perfectgift server and port config.
EXPOSE 80
CMD ["python3", "wishlist.py", "-H*", "-p80"]
