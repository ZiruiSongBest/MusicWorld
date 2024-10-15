package com.musiceg.demo.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.musiceg.demo.service.ImageGenerationService;

@RestController
@RequestMapping("/api")
public class ImageGenerationController {

    private final ImageGenerationService imageProcessingService;

    @Value("${file.upload-dir}")
    private String uploadDir;

    public ImageGenerationController(ImageGenerationService imageProcessingService) {
        this.imageProcessingService = imageProcessingService;
    }

    @PostMapping("/upload")
    public String handleFileUpload(@RequestParam("file") MultipartFile file) {
        String filePath = imageProcessingService.saveFileToLocal(file, uploadDir);

        String audioPath = imageProcessingService.runTestPyScript(filePath);

        return "Audio generated at: " + audioPath;
    }
}
