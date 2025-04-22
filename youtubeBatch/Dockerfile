# Build stage
FROM gradle:7.6.1-jdk17 AS builder
WORKDIR /app

# Copy build files first to leverage Docker cache
COPY build.gradle.kts settings.gradle.kts ./
COPY gradle ./gradle
RUN gradle dependencies --no-daemon

# Copy source code
COPY src ./src

# Build the application
RUN gradle bootJar --no-daemon

# Run stage
FROM amazoncorretto:17
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]

# FROM gradle:7.6.1-jdk17 AS build
# WORKDIR /app
# COPY . .
# RUN gradle bootJar --no-daemon

# FROM amazoncorretto:17
# WORKDIR /app
# COPY --from=build /app/build/libs/*.jar app.jar
# ENTRYPOINT ["java","-jar","app.jar"]

