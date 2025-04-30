package com.example.youtubeTrender.service

import org.springframework.stereotype.Service
import java.io.File
import java.io.FileWriter
import java.nio.file.Files
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import kotlin.reflect.KProperty1
import kotlin.reflect.full.memberProperties

//
@Service
class CsvServiceSymbolic {
    private val dateTimeFormatter = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss")
    private val MAX_KEEP_FILES = 24 // 24시간 분량의 파일만 유지

    fun <T : Any> writeDtoListToCsv(dtoList: List<T>, baseFileName: String) {
        if (dtoList.isEmpty()) return

        val directory = File("../csvCollection")
        if (!directory.exists()) {
            directory.mkdirs()
        }

        // 타임스탬프 형식: YYYYMMDD_HHmmss
        val timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"))
        val fullFileName = "${baseFileName}_$timestamp.csv"
        val file = File(directory, fullFileName)

        // CSV 파일 작성
        FileWriter(file).use { writer ->
            val clazz = dtoList.first()::class
            val properties = clazz.memberProperties.map { it as KProperty1<T, *> }

            writer.appendLine(properties.joinToString(",") { it.name })

            for (dto in dtoList) {
                val line = properties.joinToString(",") { prop ->
                    val value = prop.get(dto)?.toString() ?: ""
                    value
                        .replace("\n", " ")
                        .replace(",", " ")
                }
                writer.appendLine(line)
            }
        }

        // 최신 1개만 유지하고 나머지 삭제
        cleanupOldCsvFiles(directory, baseFileName)
    }

    fun cleanupOldCsvFiles(directory: File, baseFileName: String) {
        val matchingFiles = directory.listFiles { file ->
            file.name.matches(Regex("${baseFileName}_\\d{8}_\\d{6}\\.csv")) &&
                    !Files.isSymbolicLink(file.toPath())
        } ?: return

        val sortedFiles = matchingFiles.sortedByDescending { it.lastModified() }

        val filesToDelete = sortedFiles.drop(1)
        filesToDelete.forEach { it.delete() }
    }


//    private fun cleanupOldFiles(directory: File, baseFileName: String) {
//        val files = directory.listFiles { file ->
//            file.name.startsWith(baseFileName) && file.name.endsWith(".csv")
//        }?.sortedByDescending { it.lastModified() } ?: return
//
//        if (files.size > MAX_KEEP_FILES) {
//            files.subList(MAX_KEEP_FILES, files.size).forEach { it.delete() }
//        }
//    }
}
