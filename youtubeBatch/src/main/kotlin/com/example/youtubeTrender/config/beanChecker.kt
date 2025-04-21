//package com.example.youtubeTrender.config
//
//import org.springframework.boot.ApplicationArguments
//import org.springframework.boot.ApplicationRunner
//import org.springframework.context.ApplicationContext
//import org.springframework.stereotype.Component
//
//@Component
//class BeanChecker(private val context: ApplicationContext) : ApplicationRunner {
//    override fun run(args: ApplicationArguments?) {
//        val beanNames = context.beanDefinitionNames
//        if ("messageController" in beanNames) {
//            println("✅ MessageController is registered as a Bean!")
//        } else {
//            println("❌ MessageController is NOT registered!")
//        }
//    }
//}