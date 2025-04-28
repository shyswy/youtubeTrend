package com.example.youtubeTrender.batch.tasklet

import com.example.youtubeTrender.service.YoutubeService

import org.springframework.batch.core.step.tasklet.Tasklet
import org.springframework.batch.core.StepContribution
import org.springframework.batch.core.scope.context.ChunkContext
import org.springframework.stereotype.Component

@Component
class YoutubeTasklet(
    private val youtubeService: YoutubeService
) : Tasklet {
    override fun execute(contribution: StepContribution, chunkContext: ChunkContext): org.springframework.batch.repeat.RepeatStatus {
        youtubeService.save()
        return org.springframework.batch.repeat.RepeatStatus.FINISHED
    }
}
