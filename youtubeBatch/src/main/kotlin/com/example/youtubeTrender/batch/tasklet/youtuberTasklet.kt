package com.example.youtubeTrender.batch.tasklet

import com.example.youtubeTrender.service.YoutuberService
import kotlinx.coroutines.runBlocking
import org.springframework.batch.core.step.tasklet.Tasklet
import org.springframework.batch.core.StepContribution
import org.springframework.batch.core.scope.context.ChunkContext
import org.springframework.stereotype.Component

@Component
class YoutuberTasklet(
    private val youtuberService: YoutuberService



) : Tasklet {
    override fun execute(contribution: StepContribution, chunkContext: ChunkContext): org.springframework.batch.repeat.RepeatStatus {
        runBlocking {
            youtuberService.asyncSave()
        }
        return org.springframework.batch.repeat.RepeatStatus.FINISHED
    }
}
