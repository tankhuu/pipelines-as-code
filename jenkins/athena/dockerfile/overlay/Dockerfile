FROM 696952606624.dkr.ecr.us-east-2.amazonaws.com/openjdk11_gdal
ARG BUILD_VERSION
RUN mkdir -p /home/athena
ADD *.jar /home/athena/app.jar
EXPOSE 8076
