package com.musiceg.demo.service;

import java.io.File;
import java.io.IOException;

import org.springframework.web.multipart.MultipartFile;

public class ImageGenerationService {
     // 保存上传的文件到本地目录
    public String saveFileToLocal(MultipartFile file, String uploadDir) {
        try {
            String fileName = file.getOriginalFilename();
            String filePath = uploadDir + fileName;
            File dest = new File(filePath);
            file.transferTo(dest);  // 保存文件
            return filePath;
        } catch (IOException e) {
            throw new RuntimeException("Failed to store file", e);
        }
    }

    // 调用 test.py 脚本处理生成音频
    public String runTestPyScript(String filePath) {
        try {
            String[] command = new String[] {"python", "test.py", filePath};
            ProcessBuilder processBuilder = new ProcessBuilder(command);
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            int exitCode = process.waitFor();
            if (exitCode != 0) {
                throw new RuntimeException("Python script failed with exit code: " + exitCode);
            }

            return "C:/uploads/output_audio.wav"; // 生成的音频文件路径
        } catch (Exception e) {
            throw new RuntimeException("Failed to execute Python script", e);
        }
    }
}
