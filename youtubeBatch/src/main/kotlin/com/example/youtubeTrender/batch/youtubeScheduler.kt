package com.example.youtubeTrender.batch


import org.springframework.batch.core.Job
import org.springframework.batch.core.launch.JobLauncher
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import java.time.LocalDateTime
import org.springframework.beans.factory.annotation.Value

@Component
class BatchScheduler(
    private val jobLauncher: JobLauncher,
    private val youtubeCollectJob: Job
) {

    @Value("\${BATCH_JOB_FIXED_RATE:600000}")  // 기본값을 설정하고 환경변수에서 값을 읽음
    private lateinit var fixedRate: String
    // 데이터 양이 많을 경우, chunk-based processing과 같은 기법을 사용하여 성능을 최적화
    // https://king-ja.tistory.com/81.  Quartz 등 스케쥴러로 수정 시 retry 등 디테일 처리 가능.
   @Scheduled(fixedRateString = "\${BATCH_JOB_FIXED_RATE:600000}") 
    fun runYoutubeCollectJob() {
        val jobParameters = org.springframework.batch.core.JobParametersBuilder()
            .addLong("timestamp", System.currentTimeMillis())
            .toJobParameters()

        println("batch 주기: ${fixedRate.toLong()}")

        println("⏰ YoutubeCollectJob 시작: ${LocalDateTime.now()}")
        jobLauncher.run(youtubeCollectJob, jobParameters)
        println("⏰ YoutubeCollectJob 종료: ${LocalDateTime.now()}")
    }
}
