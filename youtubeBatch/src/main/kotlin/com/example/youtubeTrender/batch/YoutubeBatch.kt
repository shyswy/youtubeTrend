package com.example.youtubeTrender.batch

import com.example.youtubeTrender.service.CsvService
import com.example.youtubeTrender.service.YoutubeService
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

@Component
class YoutubeBatch(
    private val youtubeService: YoutubeService,
    private val csvService: CsvService
//    private val csvService: CsvServiceSymbolic

) {
    private val log = LoggerFactory.getLogger(javaClass)

    @Scheduled(fixedRate = 3600000) // 10분마다
    fun fetchPopularVideosAndCommentsBatch() {
        log.info("⏰ Youtube 영상 및 댓글 수집 배치 시작: {}", LocalDateTime.now())

        // region_category 별 인기 영상 목록 조회
        val popularVideoMap = youtubeService.fetchPopularVideosForAllRegionsAndCategories()

        val timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmm"))

        popularVideoMap.forEach { (key, videos) ->
            val videoFileName = "${key}_video"
//            val videoFileName = "${key}_video_$timestamp"
            csvService.writeDtoListToCsv(videos, videoFileName)
            println("✅ 저장 완료: $videoFileName.csv (${videos.size}개 영상)")

            log.info("getComments from $key")
            val allComments = videos.flatMap { video ->
                try {
                    youtubeService.getComments(video.id)
                } catch (e: Exception) {
                    log.error("❌ 댓글 조회 실패 - videoId: ${video.id}, 에러: ${e.message}")
                    emptyList()
                }
            }

//            val commentFileName = "${key}_comments_$timestamp"
            val commentFileName = "${key}_comments"
            csvService.writeDtoListToCsv(allComments, commentFileName)
            println("💬 댓글 저장 완료: $commentFileName.csv (${allComments.size}개 댓글)")
        }
        log.info("🎉 Youtube 영상 및 댓글 수집 배치 종료: {}", LocalDateTime.now())
    }
}
