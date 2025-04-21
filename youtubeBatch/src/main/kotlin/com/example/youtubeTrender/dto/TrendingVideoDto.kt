package com.example.youtubeTrender.dto

data class TrendingVideoDto(
    val videoId: String,
    val title: String,
    val isLive: Boolean,
    val liveChatId: String?
)
