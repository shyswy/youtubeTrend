//package com.example.youtubeTrender.controller
//
//import com.example.service.YoutubeService
//import com.example.youtubeTrender.dto.CommentDto
//import com.example.youtubeTrender.dto.LiveChatMessageDto
//import com.example.youtubeTrender.service.YoutubeApiFetcher
//import org.springframework.http.ResponseEntity
//import org.springframework.web.bind.annotation.GetMapping
//import org.springframework.web.bind.annotation.RequestMapping
//import org.springframework.web.bind.annotation.RestController
//
//@RestController
//@RequestMapping("/youtube")
//class YoutubeController(
//    private val youtubeService: YoutubeService,
//    private val youtubeApiFetcher: YoutubeApiFetcher
//) {
//
//    @GetMapping("/live-chats")
//    fun getTrendingLiveChats(): List<LiveChatMessageDto> {
//        return youtubeService.fetchTrendingLiveChats()
//    }
//
//    @GetMapping("/fetch-all")
//    fun fetchAllYoutubeData(): String {
//        youtubeApiFetcher.fetchAndSaveAll()
//        return "YouTube API data fetched and saved to ./dummyResponse"
//    }
//
//    @GetMapping("/comments")
//    fun getTrendingVideoComments(): ResponseEntity<List<CommentDto>> {
//        val comments = youtubeService.fetchTrendingVideoComments()
//        return ResponseEntity.ok(comments)
//    }
//
//}
