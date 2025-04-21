package com.example.youtubeTrender.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class TrendingVideoDto(
    @SerialName("videoId")
    val videoId: String,
    @SerialName("title")
    val title: String,
    @SerialName("isLive")
    val isLive: Boolean,
    @SerialName("liveChatId")
    val liveChatId: String?
)
