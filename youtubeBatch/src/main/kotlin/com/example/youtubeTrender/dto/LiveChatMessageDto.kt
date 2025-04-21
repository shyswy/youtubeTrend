package com.example.youtubeTrender.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class LiveChatMessageDto(
    @SerialName("author")
    val author: String,
    @SerialName("message")
    val message: String,
    @SerialName("publishedAt")
    val publishedAt: String,
    @SerialName("videoId")
    val videoId: String
)
