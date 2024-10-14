package com.musiceg.demo.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import com.musiceg.demo.service.ImageGenerationService;

import javax.sound.sampled.AudioInputStream;
import java.io.File;
import java.io.IOException;

@RestController
@RequestMapping("/api")
public class ImageGenerationController {

    private final ImageGenerationService imageProcessingService;

    // 从配置文件中读取上传目录
    @Value("${file.upload-dir}")
    private String uploadDir;

    public ImageGenerationController(ImageGenerationService imageProcessingService) {
        this.imageProcessingService = imageProcessingService;
    }

    // 路由处理图片上传并生成音频文件
    @PostMapping("/upload")
    public String handleFileUpload(@RequestParam("file") MultipartFile file) {
        // 1. 保存图片到本地
        String filePath = imageProcessingService.saveFileToLocal(file, uploadDir);

        // 2. 调用 test.py 来生成音频
        String audioPath = imageProcessingService.runTestPyScript(filePath);

        // 3. 返回生成的音频文件路径或下载链接
        return "Audio generated at: " + audioPath;
    }
}
