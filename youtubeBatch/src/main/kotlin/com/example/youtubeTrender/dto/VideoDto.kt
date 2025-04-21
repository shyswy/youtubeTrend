package com.example.youtubeTrender.dto


data class VideoDto(
    val id: String,
    val title: String,
    val channelTitle: String,
    val categoryId: String,
    val viewCount: Long
)


//data class VideoDto(
//    val videoId: String,
//    val title: String
//)
