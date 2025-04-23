package com.example.youtubeTrender.batch

import com.example.youtubeTrender.dto.YoutuberInfo
import com.example.youtubeTrender.service.CsvService
import com.example.youtubeTrender.service.YoutubeService
import com.example.youtubeTrender.service.YoutuberService
import com.example.youtubeTrender.util.RegionCategoryFetcher
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import java.time.LocalDateTime

@Component
class YoutubeBatch(
    private val youtubeService: YoutubeService,
    private val youtuberService: YoutuberService,
//    private val csvService: CsvService
//    private val csvService: CsvServiceSymbolic

) {
    private val log = LoggerFactory.getLogger(javaClass)

    @Scheduled(fixedRate = 3600000) // 10분마다
    fun fetchPopularVideosAndCommentsBatch() {
        log.info("⏰ Youtube 영상 및 댓글 수집 배치 시작: {}", LocalDateTime.now())
        
        youtuberService.save()

        youtubeService.save()
        log.info("🎉 Youtube 영상 및 댓글 수집 배치 종료: {}", LocalDateTime.now())
    }
}
