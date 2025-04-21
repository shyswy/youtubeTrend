package com.example.youtubeTrender.dto

data class LiveChatMessageDto(
    val author: String,
    val message: String,
    val publishedAt: String,
    val videoId: String
)
