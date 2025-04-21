package com.example.youtubeTrender.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class VideoDto(
    @SerialName("id")
    val id: String,
    @SerialName("title")
    val title: String,
    @SerialName("channelTitle")
    val channelTitle: String,
    @SerialName("categoryId")
    val categoryId: String,
    @SerialName("category")
    val category: String? = null,
    @SerialName("viewCount")
    val viewCount: Long,
    @SerialName("likeCount")
    val likeCount: Long? = null,
    @SerialName("description")
    val description: String? = null,
    @SerialName("tags")
    val tags: List<String>? = null,
    @SerialName("url")
    val url: String,
    @SerialName("publishedAt")
    val publishedAt: String,
    @SerialName("commentCount")
    val commentCount: Long? = null,
    @SerialName("country")
    val country: String
)