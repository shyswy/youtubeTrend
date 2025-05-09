package com.example.youtubeTrender.service

import com.example.youtubeTrender.dto.CommentDto
import kotlinx.serialization.SerialName
import org.springframework.stereotype.Service
import java.io.File
import java.io.FileWriter
import kotlin.reflect.KProperty1
import kotlin.reflect.full.findAnnotation
import kotlin.reflect.full.memberProperties

@Service
class CsvService {
    // reflection 사용해서 dto의 구성을 동적으로 읽어와 그에 알맞는 csv 파일 빌드.
    fun <T : Any> writeDtoListToCsv(dtoList: List<T>, fileName: String) {

        // DTO 리스트가 비어 있으면 함수 종료
        if (dtoList.isEmpty()) return

        // 환경 변수에서 CSV 저장 경로를 가져옴 (기본값: /data)
        val csvPath = System.getenv("CSV_DATA_PATH") ?: "./data"
        val directory = File(csvPath)

        println("[path log] csvPath: $csvPath directory: $directory")

        // 만약 디렉토리가 없으면 생성
        if (!directory.exists()) {
            directory.mkdirs()
        }

        // CSV 파일을 저장할 경로 설정 (csvCollection/파일명.csv)
        val file = File(directory, "$fileName.csv")
        // 파일 쓰기 작업을 위한 FileWriter 사용
        FileWriter(file).use { writer ->
            // 첫 번째 DTO 객체의 클래스를 가져와서 해당 클래스의 프로퍼티들을 읽어옴
            val clazz = dtoList.first()::class
            // 해당 클래스의 모든 프로퍼티(필드)들을 리플렉션으로 가져옴
            val properties = clazz.memberProperties.map { it as KProperty1<T, *> }

            // CSV 헤더 작성: @SerialName 값이 있으면 그 값을 사용하고, 없으면 프로퍼티 이름을 사용
            val headers = properties.map { prop ->
                prop.findAnnotation<SerialName>()?.value ?: prop.name
            }
            // 헤더를 쉼표로 구분해서 출력
            writer.appendLine(headers.joinToString(","))

            // DTO 리스트에 있는 각 객체에 대해 CSV 데이터 작성
            for (dto in dtoList) {
                val line = properties.joinToString(",") { prop ->
                    val rawValue = prop.get(dto)?.toString() ?: ""
                    val escapedValue = rawValue
                        .replace("\"", "\"\"") // 큰따옴표 이스케이프
                    if (escapedValue.contains(",") || escapedValue.contains("\n") || escapedValue.contains("\"")) {
                        "\"$escapedValue\"" // 특수 문자가 있다면 큰따옴표로 감싸기
                    } else {
                        escapedValue
                    }
                }
                // 변환된 데이터를 CSV 파일에 한 줄씩 작성
                writer.appendLine(line)
            }
        }
    }
}