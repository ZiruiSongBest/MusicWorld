<template>
  <div v-if="$route.path !== '/library'" class="min-h-screen flex flex-col items-end">
    <!-- Header -->
    <header class="flex justify-between items-center p-4 bg-white shadow-md w-full mx-auto">
      <div class="text-xl font-bold">Music generator</div>
      <nav class="space-x-6">
        <router-link to="/library">Go to Library</router-link>
      </nav>
      <div class="flex items-center space-x-4">
        <img src="@/assets/musichead.jpg" alt="User Avatar" class="rounded-full w-10 h-10">
        <!-- Music Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
          <path d="M12 3v10.55A4 4 0 1014 17V7h4V3h-6z"/>
        </svg>
      </div>
    </header>

    <!-- Main Content -->
    <main v-if="$route.path !== '/library'" class="flex-1 p-6 bg-gray-50 w-full max-w-screen-lg mx-auto">
      <section class="text-center mb-8">
        <h1 class="text-5xl font-bold mb-4">Music World</h1>
        <p class="text-lg text-gray-600">
          Upload audio, text, image, or video files to generate music.
        </p>
      </section>

      <img src="@/assets/music.png" alt="Music Notes" class="mx-auto mb-8 rounded-lg shadow-md">

      <section class="text-center mb-12">
        <h2 class="text-3xl font-semibold mb-4">Music generator</h2>
        <p class="text-gray-600 mb-4">Generate music through multiple input forms: audio, text, image, and video.</p>

        <!-- Input section with icons and buttons -->
        <div class="flex justify-center space-x-6 mb-6">
          
          <!-- Image input -->
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="48" height="48">
              <path d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zm-4.5-7c.83 0 1.5.67 1.5 1.5S17.33 15 16.5 15 15 14.33 15 13.5 15.67 12 16.5 12zM5 19l3.5-4.5 2.5 3.01L14.5 13l4.5 6H5z"/>
            </svg>
            <input 
              type="file" 
              id="imageFile" 
              class="absolute inset-0 opacity-0 w-full h-full" 
              @change="handleFileUpload($event, 'image')" 
              accept=".jpg, .jpeg, .png"
            >
            <label for="imageFile" class="px-4 py-2 bg-blue-600 text-white rounded-md cursor-pointer">Upload Image</label>
          </div>

          <!-- Text input -->
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="48" height="48">
              <path d="M6 2v20h12V8l-6-6H6zm7 7H9V7h4v2zm0 4H9v-2h4v2zm0 4H9v-2h4v2z"/>
            </svg>
            <input 
              type="file" 
              id="textFile" 
              class="absolute inset-0 opacity-0 w-full h-full" 
              @change="handleFileUpload($event, 'text_files')" 
              accept=".txt, .doc"
            >
            <label for="textFile" class="px-4 py-2 bg-blue-600 text-white rounded-md cursor-pointer">Upload Text</label>
          </div>

          <!-- Audio input -->
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="48" height="48">
              <path d="M12 3v10.55A4 4 0 1014 17V7h4V3h-6z"/>
            </svg>
            <input 
              type="file" 
              id="audioFile" 
              class="absolute inset-0 opacity-0 w-full h-full" 
              @change="handleFileUpload($event, 'audio')" 
              accept=".mp3, .wav"
            >
            <label for="audioFile" class="px-4 py-2 bg-blue-600 text-white rounded-md cursor-pointer">Upload Audio</label>
          </div>

          <!-- Video input -->
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="48" height="48">
              <path d="M6 18l8.5-6L6 6v12zm9-12v12h2V6h-2z"/>
            </svg>
            <input 
              type="file" 
              id="videoFile" 
              class="absolute inset-0 opacity-0 w-full h-full" 
              @change="handleFileUpload($event, 'video')" 
              accept=".mp4"
            >
            <label for="videoFile" class="px-4 py-2 bg-blue-600 text-white rounded-md cursor-pointer">Upload Video</label>
          </div>

        </div>

        <div>
          <button @click="uploadToAPI" class="px-6 py-3 bg-blue-600 text-white rounded-md">Generate music</button>
        </div>

        <div id="result-container" v-if="result">
          <pre>{{ result }}</pre>  <!-- 将结果以 JSON 格式显示 -->
        </div>
        
        <div class="flex justify-center">
          <img src="@/assets/musicbottom.jpg" alt="Music Generation Preview" class="rounded-lg shadow-md w-full max-w-3xl">
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer v-if="$route.path !== '/library'" class="bg-white p-6 shadow-inner w-full max-w-5xl mx-auto">
      <div class="flex justify-between items-center">
        <p class="text-gray-600">&copy; 2024 Music World</p>
        <div class="flex space-x-4">
          <a href="#" class="text-gray-600">About us</a>
          <a href="#" class="text-gray-600">Connection method</a>
          <a href="#" class="text-gray-600">Project culture</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFiles: {
        text_files: null,
        audio: null,
        image: null,
        video: null,
      },
      result: null, // 用于存储API返回的结果
    };
  },
  methods: {
    handleFileUpload(event, type) {
      this.selectedFiles[type] = event.target.files[0]; // 获取并存储用户选择的文件
    },
    async uploadToAPI() {
      const formData = new FormData();

      // 遍历所有文件类型，将非空的文件追加到FormData中
      for (const [key, file] of Object.entries(this.selectedFiles)) {
        if (file) {
          formData.append(key, file);  // key 即为 'text_files', 'audio', 'image', 'video'
        }
      }

      try {
        // 发送文件到API
        const response = await axios.post('https://d22a-138-25-54-191.ngrok-free.app/generate', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        // 将API返回的结果保存到result中
        this.result = response.data;
        console.log('Response data:', response.data);
      } catch (error) {
        console.error('Error uploading files:', error);
      }
    }
  }
};
</script>

<style scoped>
audio {
  display: none;
}
input[type="file"] {
  display: none;
}
</style>
