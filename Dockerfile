###############################################
# Dockerfile for the perfectgift tornado app. #
# Based on ubuntu 13.04                       #
###############################################

FROM ubuntu:13.04
MAINTAINER "cyphar <cyphar@cyphar.com>"

##################
# Update server. #
##################

# Make sure the repos and packages are up to date
RUN apt-get update
RUN apt-get upgrade -y

############################################
# Install perfectgift server dependencies. #
############################################

# Install python3 and pillow.
RUN apt-get install -y python3 python3-imaging

##########################################
# Install and configure perfectgift app. #
##########################################

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
