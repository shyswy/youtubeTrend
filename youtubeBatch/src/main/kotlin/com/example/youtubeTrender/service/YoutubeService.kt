package com.example.youtubeTrender.service

import com.example.youtubeTrender.config.YoutubeConstants
import com.example.youtubeTrender.dto.CommentDto
import com.example.youtubeTrender.dto.VideoDto
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.youtube.YouTube
import com.google.api.services.youtube.model.VideoListResponse
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import kotlin.collections.component1
import kotlin.collections.component2

private const val LG_ELECTRONICS_US = "lg electronics"

private const val LG_ELECTRONICS_KR = "LG전자"

private const val WEEKLY_CSV_IDENTIFIER = "weekly"

@Service
class YoutubeService (
    private val csvService: CsvService
) {

    private val LG_KEYWORD = mapOf(
        "KR" to LG_ELECTRONICS_KR,
        "US" to LG_ELECTRONICS_US,
    )

    @Value("\${youtube.api-key}")
    private lateinit var apiKey: String

    private val youtube: YouTube = YouTube.Builder(
        GoogleNetHttpTransport.newTrustedTransport(),
        GsonFactory.getDefaultInstance(), // JacksonFactory -> GsonFactory
        null
    ).setApplicationName("YoutubeTrender").build()


    fun save() {
        val popularVideoMap = YoutubeConstants.REGIONS.flatMap { region ->
            // 카테고리 이름과 ID를 기반으로 하는 항목들을 맵핑
            val categoryResults = YoutubeConstants.CATEGORY_MAP.map { (categoryName, categoryId) ->
                val key = "${region}_${categoryName}"
                key to getPopularVideosByRegionAndCategory(region, categoryName, categoryId)
            }

            // defaultKey 추가
            val weekKey = "${region}_weekly"
            val weekTotalData = getPopularVideosByRegionAndCategory(region, "all", null)
            categoryResults + (weekKey to weekTotalData)
        }.toMap()

        val keyWorldVideoMap = YoutubeConstants.REGIONS.associate { region ->
            "${region}_lge" to getTopVideosByKeyword(region, LG_KEYWORD[region]?: LG_ELECTRONICS_US)
        }

        val mergedVideoMap = popularVideoMap + keyWorldVideoMap

        mergedVideoMap.forEach { (key, videos) ->
            val videoFileName = "${key}_video"
            csvService.writeDtoListToCsv(videos, videoFileName)
            println("✅ 저장 완료: $videoFileName.csv (${videos.size}개 영상)")

            if (WEEKLY_CSV_IDENTIFIER in key) {
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

    fun getTopVideosByKeyword(countryCode: String = "KR", keyword: String = LG_ELECTRONICS_KR, maxVideos: Long = 50): List<VideoDto> {
        return try {
            // Step 1: Search for videos
            val searchRequest = youtube.search().list("snippet")
                .setQ(keyword)
                .setType("video")
                .setOrder("viewCount")
                .setRegionCode(countryCode)
                .setMaxResults(maxVideos)
                .setKey(apiKey)

            val searchResponse = searchRequest.execute()

            val videoIds = searchResponse.items.mapNotNull { it.id.videoId }

            if (videoIds.isEmpty()) return emptyList()

            // Step 2: Get video statistics
            val videosRequest = youtube.videos().list("snippet,statistics")
                .setId(videoIds.joinToString(","))
                .setKey(apiKey)

            val videosResponse = videosRequest.execute()

            videosResponse.items.map {
                val snippet = it.snippet
                val statistics = it.statistics
                val videoId = it.id

                VideoDto(
                    id = videoId,
                    title = snippet.title,
                    channelTitle = snippet.channelTitle,
                    categoryId = snippet.categoryId ?: "unknown",
                    category = null, // 필요시 RegionCategoryFetcher 활용
                    viewCount = statistics.viewCount?.toLong() ?: 0,
                    likeCount = statistics.likeCount?.toLong(),
                    description = snippet.description,
                    tags = snippet.tags,
                    url = "https://www.youtube.com/watch?v=$videoId",
                    publishedAt = snippet.publishedAt.toString(),
                    commentCount = statistics.commentCount?.toLong(),
                    country = countryCode
                )
            }
        } catch (e: Exception) {
            println("영상 검색 오류: ${e.message}")
            emptyList()
        }
    }
}

