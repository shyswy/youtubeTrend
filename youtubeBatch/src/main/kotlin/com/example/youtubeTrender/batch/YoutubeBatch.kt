package com.example.youtubeTrender.batch

import com.example.youtubeTrender.service.YoutubeService
import com.example.youtubeTrender.service.YoutuberService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import java.time.LocalDateTime

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*

@Component
class YoutubeBatch(
    private val youtubeService: YoutubeService,
    private val youtuberService: YoutuberService,
) {
    private val log = LoggerFactory.getLogger(javaClass)

    @Scheduled(fixedRate = 3600000)
fun fetchPopularVideosAndCommentsBatch() = runBlocking {
        log.info("⏰ Youtube 영상 및 댓글 수집 배치 시작: {}", LocalDateTime.now())

        coroutineScope {
            withContext(Dispatchers.IO) {
                youtubeService.save()
            }

            val youtuberJob = async { youtuberService.asyncSave() }
            awaitAll(youtuberJob)
        }

        val dashIp = System.getenv("DASH_IP") ?: "localhost"
        val dashPort = System.getenv("DASH_PORT") ?: "8050"
        val dashUrl = "http://$dashIp:$dashPort/refresh"
        println("[update notify] send request to $dashUrl")
        val client = HttpClient(CIO)
        val response: String = try {
            val httpResponse: HttpResponse = client.get(dashUrl)
            httpResponse.bodyAsText()
        } catch (e: Exception) {
            log.error("❌ Dash 리프레시 요청 실패: {}", e.message)
            "요청 실패: ${e.message}"
        } finally {
            client.close()
        }

        log.info("🎉 Youtube 영상 및 댓글 수집 배치 종료: {}", LocalDateTime.now())
    }
}
