package com.example.youtubeTrender.batch.job

import org.springframework.batch.core.Job
import org.springframework.batch.core.job.builder.JobBuilder
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.batch.core.Step
import org.springframework.batch.core.repository.JobRepository
import org.springframework.batch.core.repository.support.SimpleJobRepository
import org.springframework.batch.support.transaction.ResourcelessTransactionManager

@Configuration
class YoutubeCollectJobConfig(
    private val jobRepository: JobRepository, // 주입
    private val saveYoutubeStep: Step,
    private val saveYoutuberStep: Step,
    private val sendEndRequestStep: Step,
) {
    @Bean
    fun youtubeCollectJob(): Job {
        return JobBuilder("youtubeCollectJob", jobRepository)
            .start(saveYoutubeStep)
            .next(saveYoutuberStep)
            .next(sendEndRequestStep)
            .build()
    }
}


