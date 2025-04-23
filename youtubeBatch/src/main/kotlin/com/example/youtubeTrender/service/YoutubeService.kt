package com.example.youtubeTrender.service

import com.example.youtubeTrender.dto.CommentDto
import com.example.youtubeTrender.dto.VideoDto
import com.example.youtubeTrender.util.RegionCategoryFetcher
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.youtube.YouTube
import com.google.api.services.youtube.model.VideoListResponse
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import kotlin.collections.component1
import kotlin.collections.component2

@Service
class YoutubeService (
    private val csvService: CsvService
) {

    @Value("\${youtube.api-key}")
    private lateinit var apiKey: String

    private val youtube: YouTube = YouTube.Builder(
        GoogleNetHttpTransport.newTrustedTransport(),
        GsonFactory.getDefaultInstance(), // JacksonFactory -> GsonFactory
        null
    ).setApplicationName("YoutubeTrender").build()


    fun save() {
        val fetchFunc: (String, String, String?) -> List<VideoDto> =
            { region, categoryName, categoryId ->
                getPopularVideosByRegionAndCategory(region, categoryName, categoryId)
            }

        val popularVideoMap = RegionCategoryFetcher.fetchForAllRegionsAndCategoriesWithDefault(fetchFunc)

        popularVideoMap.forEach { (key, videos) ->
            val videoFileName = "${key}_video"
            csvService.writeDtoListToCsv(videos, videoFileName)
            println("✅ 저장 완료: $videoFileName.csv (${videos.size}개 영상)")

            if ("weekly" in key) {
                println("skip, 'weekly' doesn't make comment data")
                return@forEach
            }
            println("getComments from $key")
            val allComments = videos.flatMap { video ->
                try {
                    getComments(video.id)
                } catch (e: Exception) {
                    println("❌ 댓글 조회 실패 - videoId: ${video.id}, 에러: ${e.message}")
                    emptyList()
                }
            }

            val commentFileName = "${key}_comments"
            csvService.writeDtoListToCsv(allComments, commentFileName)
            println("💬 댓글 저장 완료: $commentFileName.csv (${allComments.size}개 댓글)")
        }
    }

    fun getPopularVideosByRegionAndCategory(
        regionCode: String,
        categoryName: String? = "total",
        videoCategoryId: String? = null,
        maxResults: Int = 50
    ): List<VideoDto> {
        println("regionCode: $regionCode categoryName: $categoryName, videoCategoryId: $videoCategoryId")
        return try {
            val request = youtube.videos().list("snippet,statistics") // statistics 포함 시 조회수 등 가능
                .setChart("mostPopular")
                .setRegionCode(regionCode)
                .setMaxResults(maxResults.toLong())
                .setKey(apiKey)

            // 카테고리 ID가 있을 경우 설정
            videoCategoryId?.let { request.setVideoCategoryId(it) }

            val response: VideoListResponse = request.execute()

            response.items.mapNotNull { item ->
                val id = item.id
                val snippet = item.snippet
                val title = snippet?.title
                val channelTitle = snippet?.channelTitle
                val categoryId = snippet?.categoryId
                val viewCount = item.statistics?.viewCount

                if (id != null && title != null && channelTitle != null && categoryId != null && viewCount != null) {
                    VideoDto(
                        id = id,
                        title = title,
                        channelTitle = channelTitle,
                        categoryId = categoryId,
                        category = categoryName, // 별도 API에서 category name 매핑 필요
                        viewCount = viewCount.toLong(),
                        likeCount = item.statistics.likeCount?.toLong(),
                        description = snippet.description,
                        tags = snippet.tags,
                        url = "https://www.youtube.com/watch?v=$id",
                        publishedAt = snippet.publishedAt?.toString() ?: "",
                        commentCount = item.statistics.commentCount?.toLong(),
                        country = regionCode
                    )
                } else {
                    null
                }
            }
        } catch (e: Exception) {
            // 예외 발생 시 로그 출력, 예외 처리 후 빈 리스트 반환
            println("Error fetching popular video: ${e.message}")
            emptyList() // or return null if you prefer
        }
    }

    fun getComments(videoId: String, maxComments: Int = 20): List<CommentDto> {
        return try {
            val request = youtube.commentThreads().list("snippet")
                .setVideoId(videoId)
                .setMaxResults(100)
                .setTextFormat("plainText")
                .setKey(apiKey)

            val response = request.execute()

            response.items
                .sortedByDescending { it.snippet.topLevelComment.snippet.likeCount }
                .take(maxComments)
                .map {
                    val snippet = it.snippet.topLevelComment.snippet
                    CommentDto(
                        videoId = videoId,
                        text = snippet.textDisplay,
                        likeCount = snippet.likeCount ?: 0,
                        author = snippet.authorDisplayName
                    )
                }
        } catch (e: Exception) {
            if (e.message?.contains("commentsDisabled") == true) {
                println("댓글 비활성화됨 videoId: $videoId")

            } else {
                println("댓글 오류 $videoId")
            }
            emptyList()
        }
    }

}

