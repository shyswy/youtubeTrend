//package com.example.youtubeTrender.service
//
//import com.example.youtubeTrender.dto.CommentDto
//import com.example.youtubeTrender.dto.VideoDto
//import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport
//import com.google.api.client.json.gson.GsonFactory
//import com.google.api.services.youtube.YouTube
//import com.google.api.services.youtube.model.VideoListResponse
//import org.springframework.beans.factory.annotation.Value
//import org.springframework.stereotype.Service
//
//@Service
//class YoutubeService {
//
//    @Value("\${youtube.api-key}")
//    private lateinit var apiKey: String
//
//    private val youtube: YouTube = YouTube.Builder(
//        GoogleNetHttpTransport.newTrustedTransport(),
//        GsonFactory.getDefaultInstance(), // JacksonFactory -> GsonFactory
//        null
//    ).setApplicationName("YoutubeTrender").build()
//
//    fun getPopularVideos(maxResults: Int = 50): List<VideoDto> {
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
//
//    fun getComments(videoId: String): List<CommentDto> {
//        val comments = mutableListOf<CommentDto>()
//        var nextPageToken: String? = null
//
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
