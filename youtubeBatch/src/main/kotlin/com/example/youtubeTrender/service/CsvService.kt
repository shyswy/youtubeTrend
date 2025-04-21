package com.example.youtubeTrender.service

import com.example.youtubeTrender.dto.CommentDto
import org.springframework.stereotype.Service
import java.io.File
import java.io.FileWriter
import kotlin.reflect.KProperty1
import kotlin.reflect.full.memberProperties

@Service
class CsvService {
    // reflection 사용해서 dto의 구성을 동적으로 읽어와 그에 알맞는 csv 파일 빌드.
    fun <T : Any> writeDtoListToCsv(dtoList: List<T>, fileName: String) {
        // DTO 리스트가 비어 있으면 함수 종료
        if (dtoList.isEmpty()) return

        // 현재 워킹 디렉토리 기준으로 csvCollection 폴더를 생성
        val directory = File("csvCollection")
        // 만약 csvCollection 폴더가 없으면 생성
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

            // CSV 헤더 작성: 각 프로퍼티 이름을 쉼표로 구분해서 출력
            writer.appendLine(properties.joinToString(",") { it.name })

            // DTO 리스트에 있는 각 객체에 대해 CSV 데이터 작성
            for (dto in dtoList) {
                // 각 DTO 객체의 프로퍼티 값을 CSV 형식으로 변환
                val line = properties.joinToString(",") { prop ->
                    // 리플렉션을 사용하여 해당 프로퍼티의 값을 가져옴
                    val value = prop.get(dto)?.toString() ?: ""  // 값이 null일 경우 빈 문자열 사용
                    // 값에 줄바꿈(\n)이나 쉼표(,)가 있을 경우 CSV 포맷에 맞게 정리
                    value
                        .replace("\n", " ")  // 줄바꿈을 공백으로 변경
                        .replace(",", " ")   // 쉼표를 공백으로 변경
                }
                // 변환된 데이터를 CSV 파일에 한 줄씩 작성
                writer.appendLine(line)
            }
        }
    }

}
