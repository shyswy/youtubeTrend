package com.example.youtubeTrender.batch.tasklet

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import kotlinx.coroutines.runBlocking
import org.slf4j.LoggerFactory
import org.springframework.batch.core.step.tasklet.Tasklet
import org.springframework.batch.core.StepContribution
import org.springframework.batch.core.scope.context.ChunkContext
import org.springframework.stereotype.Component

@Component
class SendRequestTasklet : Tasklet {

    private val log = LoggerFactory.getLogger(javaClass)

    override fun execute(contribution: StepContribution, chunkContext: ChunkContext): org.springframework.batch.repeat.RepeatStatus {
        runBlocking {
            val dashIp = System.getenv("DASH_IP") ?: "localhost"
            val dashPort = System.getenv("DASH_PORT") ?: "8050"
            val dashUrl = "http://$dashIp:$dashPort/refresh"
            println("[update notify] send request to $dashUrl")

            val client = HttpClient(CIO)
            try {
                val response: HttpResponse = client.get(dashUrl)
                log.info("✅ Dash 리프레시 요청 성공: {}", response.bodyAsText())
            } catch (e: Exception) {
                log.error("❌ Dash 리프레시 요청 실패: {}", e.message)
            } finally {
                client.close()
            }
        }
        return org.springframework.batch.repeat.RepeatStatus.FINISHED
    }
}
