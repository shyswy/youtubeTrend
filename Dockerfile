# 1. OpenJDK 17 사용
#FROM openjdk:17-jdk-slim
#FROM amazoncorretto:17
#FROM amazoncorretto:17
#
#WORKDIR /app
#
#COPY build/libs/ddd.jar /app/app.jar
#
#CMD ["java", "-jar", "/app/app.jar"]

FROM amazoncorretto:17
ARG JAR_FILE=build/libs/*.jar
COPY ${JAR_FILE} kopringProject.jar
ENTRYPOINT ["java","-jar","/kopringProject.jar"]

#FROM amazoncorretto:17
#
#ARG JAR_PATH=build/libs
#ARG JAR_FILE=$(ls -t ${JAR_PATH}/*.jar | head -n 1)
#
#COPY ${JAR_FILE} app.jar
#
#ENTRYPOINT ["java", "-jar", "/app.jar"]


# FROM amazoncorretto:17	#베이스 이미지 + 별칭
# COPY gradlew .	#gradlew 복사
# COPY gradle gradle	#gradle 복사
# COPY build.gradle .	#build.gradle 복사
# COPY settings.gradle .	#settings.gradle 복사
# COPY src src	#웹어플리케이션 소스 복사
# RUN chmod +x ./gradlew	#gradlew 실행 권한 부여
# RUN ./gradlew bootJar	#gradlew를 통해 실행 가능한 jar파일 생성

# FROM adoptopenjdk/openjdk11	#베이스 이미지 생성
# COPY --from=builder build/libs/*.jar app.jar

# ENTRYPOINT ["java", "-jar", "/app.jar"]
 #jar 파일 실행
# VOLUME /tmp