package com.example.youtubeTrender.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class CommentDto(
    @SerialName("video_id")
    val videoId: String,
    @SerialName("comment_text")
    val text: String,
    @SerialName("comment_likes")
    val likeCount: Long,
    @SerialName("comment_author")
    val author: String
)