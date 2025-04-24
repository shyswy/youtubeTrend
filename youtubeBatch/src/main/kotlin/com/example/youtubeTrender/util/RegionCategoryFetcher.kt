package com.example.youtubeTrender.util

import com.example.youtubeTrender.config.YoutubeConstants

object RegionCategoryFetcher {

    fun <T> fetchForAllRegionsAndCategoriesWithDefault(
        fetchFunction: (region: String, categoryName: String, categoryId: String?) -> List<T>,
        defaultKeySuffix: String = "weekly"
    ): Map<String, List<T>> {
        val result = mutableMapOf<String, List<T>>()

        for (region in YoutubeConstants.REGIONS) {
            for ((categoryName, categoryId) in YoutubeConstants.CATEGORY_MAP) {
                val key = "${region}_${categoryName}"
                println("Fetching for: $key")
                val data = fetchFunction(region, categoryName, categoryId)
                result[key] = data
            }

            val defaultKey = "${region}_$defaultKeySuffix"
            val defaultData = fetchFunction(region, "all", null)
            result[defaultKey] = defaultData
        }

        return result
    }

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
