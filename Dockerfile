FROM openjdk:8u292-jre-slim-buster

COPY server /server
WORKDIR /server
CMD ["./start.sh"]



