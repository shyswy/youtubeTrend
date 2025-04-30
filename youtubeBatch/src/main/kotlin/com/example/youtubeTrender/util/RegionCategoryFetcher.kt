package com.example.youtubeTrender.util

import com.example.youtubeTrender.config.YoutubeConstants

// run function at all region and category
// temporary deprecated
object RegionCategoryFetcher {
    fun <T> fetchForAllRegionsAndCategories(
        fetchFunction: (region: String, categoryName: String, categoryId: String?) -> List<T>,
    ): Map<String, List<T>> {
        val result = mutableMapOf<String, List<T>>()

        for (region in YoutubeConstants.REGIONS) {
            for ((categoryName, categoryId) in YoutubeConstants.CATEGORY_MAP) {
                val key = "${region}_${categoryName}"
                println("Fetching for: $key")
                val data = fetchFunction(region, categoryName, categoryId)
                result[key] = data
            }
        }

        return result
    }

    fun <T> fetchForAllRegions(
        fetchFunction: (region: String) -> List<T>,
    ): Map<String, List<T>> {
        val result = mutableMapOf<String, List<T>>()

        for (region in YoutubeConstants.REGIONS) {
            val key = region
            println("Fetching for: $key")
            val data = fetchFunction(region)
            result[key] = data
        }
        return result
    }
}
