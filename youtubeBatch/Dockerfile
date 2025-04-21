

FROM amazoncorretto:17
ARG JAR_FILE=build/libs/*.jar
COPY ${JAR_FILE} kopringProject.jar
ENTRYPOINT ["java","-jar","/kopringProject.jar"]
