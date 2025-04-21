//package com.example.youtubeTrender.service
//
//
//import com.example.youtubeTrender.dto.CommentDto
//import com.example.youtubeTrender.dto.LiveChatMessageDto
//import com.example.youtubeTrender.dto.TrendingVideoDto
//import com.google.gson.JsonParser
//import org.apache.http.client.methods.HttpGet
//import org.apache.http.impl.client.HttpClients
//import org.apache.http.util.EntityUtils
//import org.springframework.beans.factory.annotation.Value
//import org.springframework.stereotype.Service
//import java.io.File
//import java.nio.file.Files
//import java.nio.file.Paths
//
//@Service
//class YoutubeService {
//
//    @Value("\${youtube.api-key}")
//    private lateinit var apiKey: String
//
//    private val httpClient = HttpClients.createDefault()
//
//    fun fetchTrendingLiveChats(): List<LiveChatMessageDto> {
//        println("fetchTrendingLiveChats in ")
//        val trendingVideos = fetchTrendingVideos()
//        println("trendingVideos: $trendingVideos" )
//
//        trendingVideos.forEach { video ->
//            println("[video] : $video")
//        }
//
//        val liveVideos = trendingVideos.filter { it.isLive && it.liveChatId != null }
//
//        println("liveVideos: $liveVideos" )
//
//        val chatMessages = mutableListOf<LiveChatMessageDto>()
//
//        for (video in liveVideos) {
//            val messages = fetchLiveChatMessages(video)
//            chatMessages += messages
//        }
//
//        print("chatMessages:$chatMessages")
//
//        return chatMessages
//    }
//
//
//    fun fetchTrendingVideosDummy() {
//        println("fetchTrendingVideos in")
//        val apiKey = "YOUR_API_KEY" // 실제 키로 대체 필요
//        val trendingUrl = "https://www.googleapis.com/youtube/v3/videos" +
//                "?part=snippet&chart=mostPopular&regionCode=KR&maxResults=5&key=$apiKey"
//
//        val httpClient = HttpClients.createDefault()
//        val response = httpClient.execute(HttpGet(trendingUrl))
//
//        response.use { res ->
//            val entity = res.entity
//            val responseBody = EntityUtils.toString(entity, "UTF-8")
//
//            // 폴더 생성
//            val dirPath = Paths.get("./dummyResponse")
//            if (!Files.exists(dirPath)) {
//                Files.createDirectories(dirPath)
//            }
//
//            // 파일에 JSON 저장
//            val file = File("./dummyResponse/trending.json")
//            file.writeText(responseBody)
//
//            println("Response saved to ${file.absolutePath}")
//        }
//    }
//
////    fun fetchTrendingVideos() {
////        println("fetchTrendingVideos in ")
////        val trendingUrl = "https://www.googleapis.com/youtube/v3/videos" +
////                "?part=snippet&chart=mostPopular&regionCode=KR&maxResults=5&key=$apiKey"
////
////        val trendingRes = httpClient.execute(HttpGet(trendingUrl))
////        println(trendingRes)
////    }
//
//    fun fetchTrendingVideos(): List<TrendingVideoDto> {
//        println("fetchTrendingVideos in ")
//        val trendingUrl = "https://www.googleapis.com/youtube/v3/videos" +
//                "?part=snippet&chart=mostPopular&regionCode=KR&maxResults=5&key=$apiKey"
//
//        val trendingRes = httpClient.execute(HttpGet(trendingUrl))
//        println(trendingRes)
//        val trendingJson = EntityUtils.toString(trendingRes.entity)
//        val trendingRoot = JsonParser.parseString(trendingJson).asJsonObject
//
//        val videoIds = trendingRoot["items"].asJsonArray.mapNotNull {
//            it.asJsonObject["id"]?.asString
//        }
//
//        return fetchVideoDetails(videoIds)
//    }
//
//    private fun fetchVideoDetails(videoIds: List<String>): List<TrendingVideoDto> {
//        val ids = videoIds.joinToString(",")
//        val detailUrl = "https://www.googleapis.com/youtube/v3/videos" +
//                "?part=snippet,liveStreamingDetails&id=$ids&key=$apiKey"
//
//        val response = httpClient.execute(HttpGet(detailUrl))
//        val json = EntityUtils.toString(response.entity)
//        println("json: $json")
//        val root = JsonParser.parseString(json).asJsonObject
//
//        return root["items"].asJsonArray.map { item ->
//            val id = item.asJsonObject["id"].asString
//            val snippet = item.asJsonObject["snippet"].asJsonObject
//            val title = snippet["title"].asString
//            val liveDetails = item.asJsonObject["liveStreamingDetails"]?.asJsonObject
//            val chatId = liveDetails?.get("activeLiveChatId")?.asString
//
//            TrendingVideoDto(
//                videoId = id,
//                title = title,
//                isLive = chatId != null,
//                liveChatId = chatId
//            )
//        }
//    }
//
//    private fun fetchLiveChatMessages(video: TrendingVideoDto): List<LiveChatMessageDto> {
//        val messages = mutableListOf<LiveChatMessageDto>()
//        val url = "https://www.googleapis.com/youtube/v3/liveChat/messages" +
//                "?liveChatId=${video.liveChatId}&part=snippet,authorDetails&key=$apiKey"
//
//        val response = httpClient.execute(HttpGet(url))
//        val json = EntityUtils.toString(response.entity)
//        val root = JsonParser.parseString(json).asJsonObject
//
//        val items = root["items"].asJsonArray
//
//        for (item in items) {
//            val snippet = item.asJsonObject["snippet"].asJsonObject
//            val author = item.asJsonObject["authorDetails"].asJsonObject["displayName"].asString
//            val message = snippet["displayMessage"].asString
//            val time = snippet["publishedAt"].asString
//
//            messages += LiveChatMessageDto(
//                author = author,
//                message = message,
//                publishedAt = time,
//                videoId = video.videoId
//            )
//        }
//
//        return messages
//    }
//
//
//
//    fun fetchTrendingVideoComments(): List<CommentDto> {
//        val trendingVideos = fetchTrendingVideos() // 이미 존재하는 메소드 활용
//        val comments = mutableListOf<CommentDto>()
//
//        trendingVideos.forEach { video ->
//            comments += fetchCommentsByVideoId(video.videoId)
//        }
//
//        return comments
//    }
//
//    private fun fetchCommentsByVideoId(videoId: String): List<CommentDto> {
//        val comments = mutableListOf<CommentDto>()
//        var nextPageToken: String? = null
//
//        do {
//            val url = buildCommentThreadsUrl(videoId, nextPageToken)
//            val response = httpClient.execute(HttpGet(url))
//            val json = EntityUtils.toString(response.entity)
//            val root = JsonParser.parseString(json).asJsonObject
//
//            nextPageToken = root.get("nextPageToken")?.asString
//
//            val items = root["items"]?.asJsonArray ?: continue
//
//            for (item in items) {
//                val snippet = item.asJsonObject["snippet"].asJsonObject["topLevelComment"]
//                    .asJsonObject["snippet"].asJsonObject
//
//                val author = snippet["authorDisplayName"].asString
//                val message = snippet["textDisplay"].asString
//                val time = snippet["publishedAt"].asString
//
//                comments += CommentDto(
//                    videoId = videoId,
//                    author = author,
//                    message = message,
//                    publishedAt = time
//                )
//            }
//
//        } while (nextPageToken != null)
//
//        return comments
//    }
//
//    private fun buildCommentThreadsUrl(videoId: String, pageToken: String?): String {
//        val base = "https://www.googleapis.com/youtube/v3/commentThreads" +
//                "?part=snippet&videoId=$videoId&maxResults=100&key=$apiKey"
//        return if (pageToken != null) "$base&pageToken=$pageToken" else base
//    }
//
//}
