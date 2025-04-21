// CommentDto.kt
package com.example.youtubeTrender.dto

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

// 국가명_카테고리명_파일명. > 파일 14개.
// 국가, 카테고리, 날짜

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


//@Serializable
//data class CommentDto(
//    @SerialName("video_id")
//    val videoId: String,
//    @SerialName("comment_text")
//    val text: String,
//    @SerialName("comment_likes")
//    val likeCount: Long,
//    @SerialName("comment_author")
//    val author: String
//)


//@Serializable
//data class CommentDto(
//    val videoId: String,
//    val text: String,
//    val likeCount: Long,
//    val author: String
//)


//@Serializable
//data class CommentDto(
//    @SerialName("videoId")
//    val videoId: String,
//    @SerialName("text")
//    val text: String,
//    @SerialName("likeCount")
//    val likeCount: Long,
//    @SerialName("author")
//    val author: String
//)



