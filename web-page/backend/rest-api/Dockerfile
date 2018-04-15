FROM centos
MAINTAINER DangPham

# Install python and pip
RUN yum -y update
RUN yum -y install epel-release
RUN yum -y install python-pip

# Install python packages via requirements.txt
RUN mkdir /source
ADD requirements.txt /source/requirements.txt
RUN pip install -r /source/requirements.txt

# Create source code repo
RUN mkdir /Serepok
ADD . /source
WORKDIR /source

CMD python backend-api.py

EXPOSE 8010


