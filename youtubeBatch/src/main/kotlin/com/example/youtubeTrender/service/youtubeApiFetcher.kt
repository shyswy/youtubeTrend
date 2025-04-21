package com.example.youtubeTrender.service


import org.apache.http.client.methods.HttpGet
import org.apache.http.impl.client.HttpClients
import org.apache.http.util.EntityUtils
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import java.io.File
import java.nio.file.Files
import java.nio.file.Paths

@Service
class YoutubeApiFetcher {

    @Value("\${youtube.api-key}")
    private lateinit var apiKey: String

    fun fetchAndSaveAll() {
        val endpoints = listOf(
//            "videos" to "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=KR&maxResults=5&key=$apiKey",
//            "channels" to "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=UC_x5XG1OV2P6uZZ5FSM9Ttw&key=$apiKey",
//            "search" to "https://www.googleapis.com/youtube/v3/search?part=snippet&q=kpop&type=video&maxResults=5&key=$apiKey",
//            "playlists" to "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=UC_x5XG1OV2P6uZZ5FSM9Ttw&maxResults=5&key=$apiKey",
//            "playlistItems" to "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=PLBCF2DAC6FFB574DE&maxResults=5&key=$apiKey",
//            "commentThreads" to "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=Ks-_Mh1QhMc&maxResults=5&key=$apiKey",
//            "videoCategories" to "https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=KR&key=$apiKey",
//            "subscriptions" to "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId=UC_x5XG1OV2P6uZZ5FSM9Ttw&maxResults=5&key=$apiKey",
//            "activities" to "https://www.googleapis.com/youtube/v3/activities?part=snippet&channelId=UC_x5XG1OV2P6uZZ5FSM9Ttw&maxResults=5&key=$apiKey",
            "channelList" to "https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&order=viewCount&maxResults=10&key=$apiKey",
        )

        val dirPath = Paths.get("./dummyResponse")
        if (!Files.exists(dirPath)) {
            Files.createDirectories(dirPath)
        }

        val httpClient = HttpClients.createDefault()

        endpoints.forEach { (name, url) ->
            try {
                println("Fetching: $name")
                val response = httpClient.execute(HttpGet(url))
                response.use { res ->
                    val entity = res.entity
                    val body = EntityUtils.toString(entity, "UTF-8")

                    val file = File("./dummyResponse/${name}.json")
                    file.writeText(body)
                    println("Saved $name → ${file.absolutePath}")
                }
            } catch (e: Exception) {
                println("❌ Failed to fetch $name: ${e.message}")
            }
        }
    }
}
