import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
	id("org.springframework.boot") version "3.0.11"
	id("io.spring.dependency-management") version "1.1.0"
	kotlin("jvm") version "1.7.22"
	kotlin("plugin.spring") version "1.7.22"
	kotlin("plugin.jpa") version "1.7.22"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_17

repositories {
	mavenCentral()
}

dependencies {

	implementation("com.google.api-client:google-api-client:1.34.0")
	implementation("com.google.http-client:google-http-client-gson:1.40.0")
	implementation("com.fasterxml.jackson.core:jackson-databind:2.13.0")


//	implementation("com.google.apis:google-api-services-youtube:v3-rev222-1.25.0")
//	implementation("com.google.apis:google-api-services-youtube:v3-rev305-1.25.0")
	implementation ("com.google.apis:google-api-services-youtube:v3-rev183-1.22.0")
	implementation("org.apache.commons:commons-csv:1.8")
	implementation("org.springframework.batch:spring-batch-core")
	implementation("org.springframework.boot:spring-boot-starter-batch")
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
//	implementation("org.springframework.boot:spring-boot-starter-web")



	implementation("org.springframework.boot:spring-boot-starter-data-jpa")
	implementation("org.springframework.boot:spring-boot-starter-web")
//	implementation("org.springframework.boot:spring-boot-starter-batch")
	implementation("org.jetbrains.kotlin:kotlin-reflect")
	implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
//	implementation("org.springframework.kafka:spring-kafka")
	implementation("org.springframework.boot:spring-boot-starter-validation")




	implementation("mysql:mysql-connector-java:8.0.28")
	runtimeOnly("com.h2database:h2")

	implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.1.0")

	implementation("org.springframework.kafka:spring-kafka")

	implementation("com.querydsl:querydsl-jpa:5.0.0:jakarta")
	implementation("com.querydsl:querydsl-kotlin:5.0.0")

	annotationProcessor("com.querydsl:querydsl-apt:5.0.0:jakarta")

	testImplementation("org.springframework.kafka:spring-kafka-test")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testImplementation("org.springframework.batch:spring-batch-test")
	testImplementation("org.junit.jupiter:junit-jupiter-api")
	testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine")

}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs = listOf("-Xjsr305=strict")
		jvmTarget = "17"
	}
}

//tasks.withType<Jar> {
//	manifest {
//		attributes["Main-Class"] = "com.example.kafka.KopringProjectApplication"
//	}
//}

tasks.withType<Test> {
	useJUnitPlatform()
}