package com.example.youtubeTrender.service

import com.example.youtubeTrender.dto.CommentDto
import com.example.youtubeTrender.dto.VideoDto
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.youtube.YouTube
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

    fun getAllPopularVideos(maxResults: Int = 50): List<VideoDto> {
        val response: VideoListResponse = youtube.videos().list("snippet")
            .setChart("mostPopular")
            .setRegionCode("KR")
            .setMaxResults(maxResults.toLong())
            .setKey(apiKey)
            .execute()

        return response.items.mapNotNull { item ->
            val id = item.id
            val title = item.snippet?.title
            if (id != null && title != null) VideoDto(id, title) else null
        }
    }

    fun getPopularVideosByRegionAndCategory(
        regionCode: String,
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
                    viewCount = viewCount.toLong()
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
            println("댓글 오류 ($videoId): ${e.message}")
            emptyList()
        }
    }
}


//    fun getComments(videoId: String): List<CommentDto> {
//        val comments = mutableListOf<CommentDto>()
//        var nextPageToken: String? = null
//        do {
//            val request = youtube.commentThreads().list("snippet")
//                .setVideoId(videoId)
//                .setMaxResults(100L)
//                .setTextFormat("plainText")
//                .setKey(apiKey)
//                .apply {
//                    if (nextPageToken != null) setPageToken(nextPageToken)
//                }
//
//            val response = request.execute()
//
//            response.items?.forEach { item ->
//                val snippet = item.snippet
//                val topLevelComment = snippet.topLevelComment.snippet
//                val author = topLevelComment.authorDisplayName
//                val text = topLevelComment.textDisplay
//                comments.add(CommentDto(videoId, author, text))
//            }
//
//            nextPageToken = response.nextPageToken
//        } while (!nextPageToken.isNullOrEmpty())
//
//        return comments
//    }
//}




//package com.example.youtubeTrender.service
//
//import com.example.youtubeTrender.dto.CommentDto
//import com.example.youtubeTrender.dto.VideoDto
//import org.springframework.beans.factory.annotation.Value
//import org.springframework.stereotype.Service
//import org.springframework.web.client.RestTemplate
//import org.springframework.web.util.UriComponentsBuilder
//
//@Service
//class YoutubeService {
//    @Value("\${youtube.api-key}")
//    private lateinit var apiKey: String
//    private val restTemplate = RestTemplate()
//
//    fun getPopularVideos(maxResults: Int = 50): List<VideoDto> {
//        val uri = UriComponentsBuilder.fromHttpUrl("https://www.googleapis.com/youtube/v3/videos")
//            .queryParam("part", "snippet")
//            .queryParam("chart", "mostPopular")
//            .queryParam("regionCode", "KR")
//            .queryParam("maxResults", maxResults)
//            .queryParam("key", apiKey)
//            .toUriString()
//
//        val response = restTemplate.getForObject(uri, Map::class.java)
//        val items = response?.get("items") as? List<Map<String, Any>> ?: return emptyList()
//
//        return items.mapNotNull { item ->
//            val id = item["id"] as? String
//            val snippet = item["snippet"] as? Map<*, *>
//            val title = snippet?.get("title") as? String
//            if (id != null && title != null) VideoDto(id, title) else null
//        }
//    }
//
//    fun getComments(videoId: String): List<CommentDto> {
//        var comments = mutableListOf<CommentDto>()
//        var nextPageToken: String? = null
//
//        do {
//            val uri = UriComponentsBuilder.fromHttpUrl("https://www.googleapis.com/youtube/v3/commentThreads")
//                .queryParam("part", "snippet")
//                .queryParam("videoId", videoId)
//                .queryParam("maxResults", 100)
//                .queryParam("key", apiKey)
//                .apply {
//                    if (nextPageToken != null) queryParam("pageToken", nextPageToken)
//                }
//                .toUriString()
//
//            val response = restTemplate.getForObject(uri, Map::class.java)
//            val items = response?.get("items") as? List<Map<String, Any>> ?: emptyList()
//
//            val newComments = items.mapNotNull { item ->
//                val snippet = (item["snippet"] as? Map<*, *>)?.get("topLevelComment") as? Map<*, *>
//                val snippetDetail = snippet?.get("snippet") as? Map<*, *>
//                val author = snippetDetail?.get("authorDisplayName") as? String
//                val text = snippetDetail?.get("textDisplay") as? String
//                if (author != null && text != null) CommentDto(videoId, author, text) else null
//            }
//
//            comments.addAll(newComments)
//            nextPageToken = response?.get("nextPageToken") as? String
//        } while (!nextPageToken.isNullOrEmpty())
//
//        return comments
//    }
//}
