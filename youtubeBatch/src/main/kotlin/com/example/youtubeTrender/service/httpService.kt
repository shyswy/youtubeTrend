package com.example.youtubeTrender.service

import com.example.youtubeTrender.dto.CommentDto
import io.ktor.client.HttpClient
import io.ktor.client.engine.cio.CIO
import io.ktor.client.request.get
import io.ktor.client.statement.HttpResponse
import io.ktor.client.statement.bodyAsText
import io.ktor.http.HttpStatusCode
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service

@Service
class HttpService {
    private val log = LoggerFactory.getLogger(javaClass)
    public suspend fun sendDoneRequest() {
        val dashIp = System.getenv("DASH_IP") ?: "localhost"
        val dashPort = System.getenv("DASH_PORT") ?: "8050"
        val dashUrl = "http://$dashIp:$dashPort/refresh"
        println("[update notify] send request to $dashUrl")

        val client = HttpClient(CIO)
        try {
            val response: HttpResponse = client.get(dashUrl)
            // Check if the response status is 200 OK
            if (response.status != HttpStatusCode.OK) {
                throw Exception("Unexpected response status: ${response.status}")
            }
            log.info("✅ Dash 리프레시 요청 성공: {}", response.bodyAsText())
        } catch (e: Exception) {
            log.error("❌ Dash 리프레시 요청 실패: {}", e.message)
            throw e
        } finally {
            client.close()
        }
    }
}