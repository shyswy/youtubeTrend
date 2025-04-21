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
) {
    private val log = LoggerFactory.getLogger(javaClass)

//    @Scheduled(fixedRate = 3600000) // 1시간마다 실행 (단위: 밀리초)
@Scheduled(fixedRate = 600000) // 1분마다 (단위: 밀리초)
fun fetchPopularCommentsBatch() {
    //
        log.info("⏰ Youtube 댓글 수집 배치 시작: {}", LocalDateTime.now())

    // 아래에서 비디오 카테고리, 국가 전체 가져오도록 수정함. 아래 getPopularVideosByRegionAndCategory 사용하도록...
    // 이거로 2*7 개 카테고리 에 대해 csv 파일 만들도록.
        val popularVideos = youtubeService.getAllPopularVideos(50)
//    val popularVideos = youtubeService.getPopularVideosByRegionAndCategory(50)

    println("[popVidoes]:$popularVideos")
        val allComments = popularVideos.flatMap { video ->
            try {
                youtubeService.getComments(video.id)
            } catch (e: Exception) {
                log.error("❌ 댓글 조회 실패 - videoId: ${video.id}, 에러: ${e.message}")
                emptyList()
            }
        }
        // 나라_카테고리이름_videos

        println("allComments")
        println(allComments)

        val timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmm"))
        // 해당 위치에 저장.
        // 국가_
        val fileName = "comments_$timestamp"
        csvService.writeDtoListToCsv(allComments, fileName)

        println("✅ 수집 완료. 총 ${allComments.size}개 댓글 저장 -> $fileName")
    }
}
