import org.springframework.batch.core.job.builder.JobBuilder
import org.springframework.batch.core.step.builder.StepBuilder
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing
import org.springframework.batch.core.launch.support.RunIdIncrementer
import org.springframework.batch.core.repository.JobRepository
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.transaction.PlatformTransactionManager
import org.springframework.batch.core.Job
import org.springframework.batch.core.Step

@Configuration
@EnableBatchProcessing
class BatchConfig {

    @Bean
    fun job(jobRepository: JobRepository, step: Step): Job {
        return JobBuilder("youtubeCommentsJob", jobRepository)
            .incrementer(RunIdIncrementer())
            .start(step)
            .build()
    }
}
