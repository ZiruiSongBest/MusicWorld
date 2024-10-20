import axios from 'axios';

// 上传文件的函数
async function uploadFiles(textPrompt, textFiles, audioFiles, imageFiles, videoFiles) {
  const formData = new FormData();

  // 添加文本提示（可选）
  if (textPrompt) {
    formData.append('text_prompt', textPrompt);
  }

  // 添加文件
  if (textFiles) {
    textFiles.forEach(file => {
      formData.append('text_files', file);
    });
  }

  if (audioFiles) {
    audioFiles.forEach(file => {
      formData.append('audio', file);
    });
  }

  if (imageFiles) {
    imageFiles.forEach(file => {
      formData.append('image', file);
    });
  }

  if (videoFiles) {
    videoFiles.forEach(file => {
      formData.append('video', file);
    });
  }

  try {
    // 发送 POST 请求到 FastAPI
    const response = await axios.post('http://localhost:8000/generate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      // 设置cookie，确保后端能拿到user_id
      withCredentials: true
    });
    
    console.log('Response data:', response.data);
    return response.data;  // 处理返回的响应数据
  } catch (error) {
    console.error('Error uploading files:', error);
  }
}
