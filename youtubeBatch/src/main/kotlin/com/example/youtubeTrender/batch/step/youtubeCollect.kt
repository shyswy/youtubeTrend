package com.example.youtubeTrender.batch.step


import com.example.youtubeTrender.batch.tasklet.SendRequestTasklet
import com.example.youtubeTrender.batch.tasklet.YoutubeTasklet
import com.example.youtubeTrender.batch.tasklet.YoutuberTasklet
import org.springframework.batch.core.Step
import org.springframework.batch.core.repository.JobRepository
import org.springframework.batch.core.step.builder.StepBuilder
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.batch.support.transaction.ResourcelessTransactionManager
@Configuration
class YoutubeCollectStepConfig(
    private val jobRepository: JobRepository // 주입
) {

    // step 별 트랜잭션 관리에 용이.
    @Bean
    fun saveYoutubeStep(youtubeTasklet: YoutubeTasklet): Step {
        return StepBuilder("saveYoutubeStep", jobRepository)
            .tasklet(youtubeTasklet, ResourcelessTransactionManager())
            .build()
    }

    @Bean
    fun saveYoutuberStep(youtuberTasklet: YoutuberTasklet): Step {
        return StepBuilder("saveYoutuberStep", jobRepository)
            .tasklet(youtuberTasklet, ResourcelessTransactionManager())
            .build()
    }

    @Bean
    fun sendEndRequestStep(sendEndRequestTasklet: SendRequestTasklet): Step {
        return StepBuilder("sendEndRequestStep", jobRepository)
            .tasklet(sendEndRequestTasklet, ResourcelessTransactionManager())
            .build()
    }
}
