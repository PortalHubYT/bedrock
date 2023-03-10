FROM amazoncorretto:17

COPY server /server
WORKDIR /server
CMD ["./start.sh"]