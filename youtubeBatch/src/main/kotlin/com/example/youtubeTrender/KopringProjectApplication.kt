package com.example.youtubeTrender

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.scheduling.annotation.EnableScheduling


//https://dodop-blog.tistory.com/427
// 특정 메시지만 필터링 +


//https://blogger903.tistory.com/42

// DLT (DLQ)
@SpringBootApplication
@EnableScheduling
//@ComponentScan("com.example")  // 컨트롤러 패키지 지정
//@EnableJpaAuditing
//@EnableJpaRepositories(basePackages = ["com.example.clubsite.repository"]) //@Import(TraceAspect.class)
class KopringProjectApplication
fun main(args: Array<String>) {
	runApplication<KopringProjectApplication>(*args)
}


/*
Message 0 is from partition: 0, thread: org.springframework.kafka.KafkaListenerEndpointContainer#0-0-C-1
Message 0 is from partition: 0, thread: org.springframework.kafka.KafkaListenerEndpointContainer#0-0-C-1
 */

