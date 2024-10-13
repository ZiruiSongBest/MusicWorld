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
        <!-- Music Icon (Replaced with SVG) -->
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
          I am an experienced web interface designer and I have designed a music generator based on your requirement.
          The generator can take three forms of input such as audio, text, and image and generate music by clicking a button.
        </p>
      </section>

      <img src="@/assets/music.png" alt="Music Notes" class="mx-auto mb-8 rounded-lg shadow-md">

      <section class="text-center mb-12">
        <h2 class="text-3xl font-semibold mb-4">Music generator</h2>
        <p class="text-gray-600 mb-4">Generate music through three input forms: audio, text, and image</p>
        <div class="flex justify-center space-x-4 mb-6">
          <button class="px-6 py-3 bg-blue-600 text-white rounded-md">Generate music</button>
          <button class="px-6 py-3 bg-gray-200 text-gray-600 rounded-md">Regenerate</button>
        </div>
        <div class="mb-3">
          <label class="block text-gray-600">Supported formats: .mp4, .txt, .doc, .jpg</label>
          <div class="relative mt-2">
            <input type="file" id="file" class="absolute inset-0 opacity-0 w-full h-full">
            <label for="file" class="px-4 py-2 bg-blue-600 text-white rounded-md cursor-pointer">Upload File</label>
          </div>
        </div>

        <div class="flex justify-center space-x-6">
          <div class="text-center">
            <!-- Replaced audio icon with SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="48" height="48">
              <path d="M12 3v10.55A4 4 0 1014 17V7h4V3h-6z"/>
            </svg>
            <p class="text-gray-600">Image input</p>
          </div>
          <div class="text-center">
            <!-- Replaced text file icon with SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="48" height="48">
              <path d="M6 2v20h12V8l-6-6H6zm7 7H9V7h4v2zm0 4H9v-2h4v2zm0 4H9v-2h4v2z"/>
            </svg>
            <p class="text-gray-600">Text input</p>
          </div>
        </div>
      </section>

      <div class="flex justify-center">
        <img src="@/assets/musicbottom.jpg" alt="Music Generation Preview" class="rounded-lg shadow-md w-full max-w-3xl">
      </div>
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
        <div class="flex space-x-4">
          <!-- Replaced social media icons with SVG -->
          <!-- <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <path d="M12 2.04C6.5 2.04 2 6.53 2 12.04 2 16.92 5.66 21.06 10.22 21.94c.75.13 1.02-.33 1.02-.73v-2.52c-4.17.94-5.05-2.01-5.05-2.01-.68-1.73-1.65-2.19-1.65-2.19-1.35-.94.11-.92.11-.92 1.5.11 2.28 1.53 2.28 1.53 1.34 2.28 3.51 1.62 4.37 1.24.13-.97.52-1.61.94-1.98-3.32-.38-6.81-1.66-6.81-7.41 0-1.64.59-2.98 1.55-4.03-.16-.38-.67-1.92.14-4.01 0 0 1.26-.4 4.12 1.52a14.36 14.36 0 017.5 0c2.86-1.92 4.12-1.52 4.12-1.52.81 2.09.3 3.63.14 4.01.96 1.05 1.55 2.39 1.55 4.03 0 5.77-3.5 7.02-6.84 7.38.54.46 1.02 1.39 1.02 2.8v4.15c0 .41.27.87 1.04.73 4.56-.88 8.22-5.02 8.22-9.9 0-5.5-4.5-10-10-10z"/>
          </svg> -->
        </div>
      </div>
    </footer>
  </div>

  <div v-if="$route.path !== '/library'" class="min-h-screen flex flex-col items-center justify-center">
    <!-- Audio Player -->
    <div class="w-full max-w-screen-lg p-4 bg-gray-100 fixed bottom-0 left-1/2 transform -translate-x-1/2 flex justify-between items-center shadow-md">
      <button @click="togglePlayPause" class="bg-blue-600 text-white px-4 py-2 rounded-md flex items-center justify-center">
        <!-- Play/Pause Icon Replaced with SVG -->
        <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
          <path d="M8 5v14l11-7z"/>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
        </svg>
      </button>
      <button class="bg-blue-700 text-white px-4 py-2 rounded-md flex items-center justify-center">
        <!-- Next Button Icon Replaced with SVG -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
          <path d="M6 18l8.5-6L6 6v12zm9-12v12h2V6h-2z"/>
        </svg>
      </button>
      <div class="flex items-center space-x-4">
        <span>{{ currentTimeDisplay }}</span>
        <input 
          type="range" 
          min="0" 
          :max="audioDuration" 
          step="0.1" 
          v-model="currentTime" 
          @input="onTimeChange" 
          class="w-64"
        />
        <span>{{ durationDisplay }}</span>
      </div>
    </div>


    <audio ref="audio" @timeupdate="updateCurrentTime" @loadedmetadata="setDuration">
      <source src="@/assets/Embrace_Darkness.mp3" type="audio/mpeg" />
      Your browser does not support the audio tag.
    </audio>
  </div>
  <main class="flex-1 p-6 bg-gray-50 w-full max-w-5xl mx-auto pb-20">
  <!-- 其他内容 -->
  </main>

</template>

<script>
export default {
  data() {
    return {
      isPlaying: false,
      currentTime: 0,
      audioDuration: 0,
    };
  },
  computed: {
    currentTimeDisplay() {
      return this.formatTime(this.currentTime);
    },
    durationDisplay() {
      return this.formatTime(this.audioDuration);
    },
  },
  methods: {
    togglePlayPause() {
      const audio = this.$refs.audio;
      if (audio.paused) {
        audio.play();
        this.isPlaying = true;
      } else {
        audio.pause();
        this.isPlaying = false;
      }
    },
    updateCurrentTime() {
      this.currentTime = this.$refs.audio.currentTime;
    },
    onTimeChange() {
      this.$refs.audio.currentTime = this.currentTime;
    },
    setDuration() {
      this.audioDuration = this.$refs.audio.duration;
    },
    formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60).toString().padStart(2, '0');
      return `${minutes}:${seconds}`;
    },
  },
};
</script>

<style scoped>
audio {
  display: none;
}
</style>