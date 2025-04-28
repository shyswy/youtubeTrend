package com.example.youtubeTrender.batch.tasklet

import com.example.youtubeTrender.service.HttpService
import com.example.youtubeTrender.service.YoutuberService
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import kotlinx.coroutines.runBlocking
import org.slf4j.LoggerFactory
import org.springframework.batch.core.step.tasklet.Tasklet
import org.springframework.batch.core.StepContribution
import org.springframework.batch.core.scope.context.ChunkContext
import org.springframework.batch.repeat.RepeatStatus
import org.springframework.stereotype.Component

@Component
class SendRequestTasklet(
    private val httpService: HttpService
) : Tasklet {

    private val log = LoggerFactory.getLogger(javaClass)

    override fun execute(contribution: StepContribution, chunkContext: ChunkContext): org.springframework.batch.repeat.RepeatStatus {
        runBlocking {
            httpService.sendDoneRequest()
        }
        return RepeatStatus.FINISHED
    }
}
