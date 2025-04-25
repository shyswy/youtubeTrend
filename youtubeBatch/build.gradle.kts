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

	// 직렬화, 역직렬화
	implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.5.0")

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

	implementation("com.opencsv:opencsv:5.7.1")

	// crawl
	implementation("org.jsoup:jsoup:1.15.4") // 최신 버전 확인


	// async ( webflux )
	implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
	implementation("org.jetbrains.kotlinx:kotlinx-coroutines-jdk8:1.7.3") // Java 8+ 환경일 경우

	// Spring 환경에서 사용할 경우 추가
	implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor:1.7.3") // Reactor 연동 (Webflux 등)

	// 비동기 http요청 ktor
	implementation("io.ktor:ktor-client-core:2.3.0") // Ktor 클라이언트의 핵심 라이브러리
	implementation("io.ktor:ktor-client-cio:2.3.0")  // CIO 엔진 (비동기 HTTP 요청을 위한 엔진)
	implementation("io.ktor:ktor-client-json:2.3.0") // JSON 처리
	implementation("io.ktor:ktor-client-serialization:2.3.0") // JSON 직렬화 지원

}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs = listOf("-Xjsr305=strict")
		jvmTarget = "17"
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}