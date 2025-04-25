package com.example.youtubeTrender.config


import io.ktor.client.*
import io.ktor.client.engine.cio.*
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class KtorClientConfig {
    @Bean
    fun httpClient(): HttpClient = HttpClient(CIO)
}