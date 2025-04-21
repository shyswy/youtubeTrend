package com.example.youtubeTrender.service

import com.example.youtubeTrender.dto.CommentDto
import com.example.youtubeTrender.dto.VideoDto
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.youtube.YouTube
import com.google.api.services.youtube.model.Video
import com.google.api.services.youtube.model.VideoListResponse
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

@Service
class YoutubeService {

    @Value("\${youtube.api-key}")
    private lateinit var apiKey: String

    private val youtube: YouTube = YouTube.Builder(
        GoogleNetHttpTransport.newTrustedTransport(),
        GsonFactory.getDefaultInstance(), // JacksonFactory -> GsonFactory
        null
    ).setApplicationName("YoutubeTrender").build()


//    fun getAllPopularVideos(maxResults: Int = 50): List<VideoDto> {
//        val response: VideoListResponse = youtube.videos().list("snippet")
//            .setChart("mostPopular")
//            .setRegionCode("KR")
//            .setMaxResults(maxResults.toLong())
//            .setKey(apiKey)
//            .execute()
//
//        return response.items.mapNotNull { item ->
//            val id = item.id
//            val title = item.snippet?.title
//            if (id != null && title != null) VideoDto(id, title) else null
//        }
//    }

    fun fetchPopularVideosForAllRegionsAndCategories(): Map<String, List<VideoDto>> {
        val regions = listOf("KR", "US")
//        val regions = listOf("KR")

        val categoryMap = mapOf(
            "all" to null,
            "music" to "10",
            "sports" to "17",
            "people_blogs" to "22",
            "comedy" to "23",
            "entertainment" to "24",
            "news" to "25"
            //            "travel_style" to "19",
        )

        val result = mutableMapOf<String, List<VideoDto>>()

        for (region in regions) {
            for ((categoryName, categoryId) in categoryMap) {
                val key = "${region}_${categoryName}"
                println("Fetching for: $key")
                val videos = getPopularVideosByRegionAndCategory(region, categoryName, categoryId)
                result[key] = videos
            }
        }

        return result
    }



    fun getPopularVideosByRegionAndCategory(
        regionCode: String,
        categoryName: String?,
        videoCategoryId: String?,
        maxResults: Int = 50
    ): List<VideoDto> {
        val request = youtube.videos().list("snippet,statistics") // statistics 포함 시 조회수 등 가능
            .setChart("mostPopular")
            .setRegionCode(regionCode)
            .setMaxResults(maxResults.toLong())
            .setKey(apiKey)

        // 카테고리 ID가 있을 경우 설정
        videoCategoryId?.let { request.setVideoCategoryId(it) }

        val response: VideoListResponse = request.execute()

        return response.items.mapNotNull { item ->
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
//                println("댓글 비활성화됨 ($videoId): ${e.message}")
                println("댓글 비활성화됨 videoId: ($videoId)")

            } else {
                println("댓글 오류 ($videoId): ${e.message}")
            }
            emptyList()
        }
    }


//    fun getComments(videoId: String, maxComments: Int = 20): List<CommentDto> {
//        return try {
//            println(" vid: $videoId")
//            val request = youtube.commentThreads().list("snippet")
//                .setVideoId(videoId)
//                .setMaxResults(100)
//                .setTextFormat("plainText")
//                .setKey(apiKey)
//
//            val response = request.execute()
//
//            response.items
//                .sortedByDescending { it.snippet.topLevelComment.snippet.likeCount }
//                .take(maxComments)
//                .map {
//                    val snippet = it.snippet.topLevelComment.snippet
//                    CommentDto(
//                        videoId = videoId,
//                        text = snippet.textDisplay,
//                        likeCount = snippet.likeCount ?: 0,
//                        author = snippet.authorDisplayName
//                    )
//                }
//        } catch (e: Exception) {
//            println("댓글 오류 ($videoId): ${e.message}")
//            emptyList()
//        }
//    }
}

