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



//data class VideoDto(
//    val id: String,
//    val title: String,
//    val channelTitle: String,
//    val categoryId: String,
//    val category: String?, // 유튜브 Video Category API로 매핑 필요
//    val viewCount: Long,
//    val likeCount: Long?,
//    val description: String?,
//    val tags: List<String>?,
//    val url: String,
//    val publishedAt: String,
//    val commentCount: Long?,
//    val country: String
//)


// video_id,title,channel,category_id,category,views,likes,description,tags,url,published_at,comment_count,country
//data class VideoDto(
//    val id: String,
//    val title: String,
//    val channelTitle: String,
//    val categoryId: String,
//    val viewCount: Long
//)


//data class VideoDto(
//    val videoId: String,
//    val title: String
//)
