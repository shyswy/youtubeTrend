// VideoDetailDto.kt
package com.example.youtubeTrender.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class VideoDetailDto(
    @SerialName("videoId")
    val videoId: String,
    @SerialName("title")
    val title: String,
    @SerialName("channelTitle")
    val channelTitle: String,
    @SerialName("publishedAt")
    val publishedAt: String
)
