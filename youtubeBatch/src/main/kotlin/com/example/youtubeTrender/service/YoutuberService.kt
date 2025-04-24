package com.example.youtubeTrender.service

import com.example.youtubeTrender.config.YoutubeConstants
import com.example.youtubeTrender.dto.YoutuberInfo
import com.example.youtubeTrender.util.RegionCategoryFetcher
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import org.springframework.stereotype.Service
import kotlin.collections.component1
import kotlin.collections.component2
import kotlin.collections.plus

@Service
class YoutuberService (
    private val csvService: CsvService
){
    private val categoryType = mapOf(
        "all" to "all",
        "entertainment" to "entertainment",
        "news" to "news",
        "people_blogs" to "vlog",
        "music" to "music",
        "comedy" to "comedy",
        "sports" to "sports"
    )

    private val rankingType = mapOf(
        "인기" to "popular",
        "구독자" to "subscribed",
        "슈퍼챗" to "superchatted",
        "라이브 시청자" to "watched",
        "조회수" to "viewed",
        "구독자 급상승" to "growth",
        "구독자 급하락" to "decline"
    )

    private val countryType = mapOf(
        "all" to "worldwide",
        "kr" to "south-korea",
        "us" to "united-states"
    )

    private val durationType = mapOf(
        "일간" to "daily",
        "주간" to "weekly",
        "월간" to "monthly",
        "연말" to "yearend",
        "연간" to "yearly",
        "전체" to "total"
    )

    fun save() {
        val youtuberRankingMap = YoutubeConstants.REGIONS.flatMap { region ->
            // 카테고리 이름과 ID를 기반으로 하는 항목들을 맵핑
            YoutubeConstants.CATEGORY_MAP.map { (categoryName, categoryId) ->
                val key = "${region}_${categoryName}"
                key to getYoutuberRanking(
                    category = categoryName,
                    country = region.lowercase(),
                    ranking = "인기",
                    duration = "주간")
            }
        }.toMap()

        youtuberRankingMap.forEach { (key, videos) ->
            val fileName = "${key}_youtuber"
            csvService.writeDtoListToCsv(videos, fileName)
            println("✅ 저장 완료: $fileName.csv (${videos.size}개 영상)")
        }
    }

    fun getYoutuberRanking(
        category: String = "all",
        country: String = "korea",
        ranking: String = "인기",
        duration: String = "일간"
    ): List<YoutuberInfo> {
        println("category: $category, country: $country, ranking: $ranking, duration: $duration")
        val categoryKey = categoryType[category] ?: "all"
        val rankingKey = rankingType[ranking] ?: "popular"
        val countryKey = countryType[country] ?: "south-korea"
        val durationKey = durationType[duration] ?: "daily"

        println("categoryKey: $categoryKey, rankingKey: $rankingKey, countryKey: $countryKey, durationKey: $durationKey")

        val url =
            "https://playboard.co/youtube-ranking/most-$rankingKey-$categoryKey-channels-in-$countryKey-$durationKey"

        return fetchRankingData(url)
    }

    private fun fetchRankingData(url: String): List<YoutuberInfo> {
        println("Fetching: $url")

        val document = fetchDocument(url)
        val rows = document.select(".chart__row")
        val result = mutableListOf<YoutuberInfo>()

        for ((index, row) in rows.withIndex()) {
            try {
                if (row.hasClass("chart__row--ad")) continue
                var item = parseRow(row)

                if (item.channelName.isNullOrBlank() || item.channelLink.isNullOrBlank()) {
                    println("[Retry] Row $index is missing data. Retrying...")
                    val retryDoc = fetchDocument(url)
                    val retryRow = retryDoc.select(".chart__row").getOrNull(index)
                    if (retryRow != null && !retryRow.hasClass("chart__row--ad")) {
                        item = parseRow(retryRow)
                    }
                }

                result.add(item)

            } catch (e: Exception) {
                println("[Error] Row $index: ${e.message}")
                result.add(YoutuberInfo(null, null, null, null, null, null))
            }
        }

        return result
    }

    private fun fetchDocument(url: String): Document {
        return Jsoup.connect(url)
            .userAgent("Mozilla/5.0")
            .get()
    }

    private fun parseRow(row: Element): YoutuberInfo {
        val rank = row.selectFirst("td.rank div.current")?.text()

        val logoTd = row.selectFirst("td.logo")
        val channelLink = logoTd?.selectFirst("a")?.attr("href")
        val channelImage = logoTd?.selectFirst("img")?.let {
            it.attr("data-src").ifEmpty { it.attr("src") }
        }

        val channelName = row.selectFirst("td.name h3")?.text()

        val videoLink = row.selectFirst("td.videos a")?.attr("href")
        var thumbnailUrl = row.selectFirst("td.videos a div.thumb")?.attr("data-background-image")
        if (thumbnailUrl?.startsWith("//") == true) {
            thumbnailUrl = "https:$thumbnailUrl"
        }

        return YoutuberInfo(
            rank = rank,
            channelName = channelName,
            channelLink = channelLink?.let { "https://youtube.com$it" },
            channelImage = channelImage,
            videoLink = videoLink?.let { "https://youtube.com$it" },
            thumbnailUrl = thumbnailUrl
        )
    }
}
