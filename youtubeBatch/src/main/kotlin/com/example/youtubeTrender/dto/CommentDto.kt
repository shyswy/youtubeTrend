// CommentDto.kt
package com.example.youtubeTrender.dto

// 국가명_카테고리명_파일명. > 파일 14개.
data class CommentDto(
    val videoId: String,
    val text: String,
    val likeCount: Long,
    val author: String
)



