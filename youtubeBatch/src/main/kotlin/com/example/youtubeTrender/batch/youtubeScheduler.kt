package com.example.youtubeTrender.batch


import org.springframework.batch.core.Job
import org.springframework.batch.core.launch.JobLauncher
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import java.time.LocalDateTime

@Component
class BatchScheduler(
    private val jobLauncher: JobLauncher,
    private val youtubeCollectJob: Job
) {
    // 데이터 양이 많을 경우, chunk-based processing과 같은 기법을 사용하여 성능을 최적화
    // https://king-ja.tistory.com/81.  Quartz 등 스케쥴러로 수정 시 retry 등 디테일 처리 가능.
    @Scheduled(fixedRate = 3600000)
    fun runYoutubeCollectJob() {
        val jobParameters = org.springframework.batch.core.JobParametersBuilder()
            .addLong("timestamp", System.currentTimeMillis())
            .toJobParameters()

        println("⏰ YoutubeCollectJob 시작: ${LocalDateTime.now()}")
        jobLauncher.run(youtubeCollectJob, jobParameters)
    }
}
