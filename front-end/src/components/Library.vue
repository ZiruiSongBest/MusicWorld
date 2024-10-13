<template>
  <div class="library-container min-h-screen p-6 bg-gray-50 w-full max-w-5xl mx-auto">
    <h1 class="text-4xl font-bold mb-6 text-center">Generated Music Library</h1>

    <!-- Music Bars -->
    <div v-if="musicList.length > 0" class="space-y-4">
      <div 
        v-for="(music, index) in musicList" 
        :key="index" 
        class="flex items-center justify-between bg-white shadow-md rounded-lg p-4 border border-gray-200">
        
        <!-- Music Info -->
        <div class="flex items-center space-x-4">
          <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="36" height="36">
            <path d="M12 3v10.55A4 4 0 1014 17V7h4V3h-6z"/>
          </svg>
          <div>
            <p class="font-bold text-lg">{{ music.name }}</p>
            <p class="text-gray-500">{{ formatTime(music.duration) }}</p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center space-x-4">
          <button 
            @click="playPauseMusic(index)" 
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center justify-center transition-colors">
            <svg v-if="currentPlayingIndex !== index || isPaused" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
              <path d="M8 5v14l11-7z"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
          </button>
          <button 
            @click="removeMusic(index)" 
            class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors">
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- No Music Message -->
    <div v-else class="text-center text-gray-600 mt-12">
      <p>No generated music available. Please generate some music first!</p>
    </div>

    <!-- Hidden audio element for playback -->
    <audio ref="audio" @ended="onMusicEnd"></audio>
  </div>
</template>

<script>
export default {
  data() {
    return {
      musicList: [
        // Example music data, replace with real data in your application
        { name: "Generated Song 1", url: "@/assets/music1.mp3", duration: 180 },
        { name: "Generated Song 2", url: "@/assets/music2.mp3", duration: 210 },
        { name: "Generated Song 3", url: "@/assets/music3.mp3", duration: 240 },
      ],
      currentPlayingIndex: null,
      isPaused: true,
    };
  },
  methods: {
    playPauseMusic(index) {
      const audio = this.$refs.audio;

      if (this.currentPlayingIndex === index) {
        // If the same song is clicked, toggle play/pause
        if (audio.paused) {
          audio.play();
          this.isPaused = false;
        } else {
          audio.pause();
          this.isPaused = true;
        }
      } else {
        // Play a new song
        this.currentPlayingIndex = index;
        audio.src = this.musicList[index].url;
        audio.play();
        this.isPaused = false;
      }
    },
    removeMusic(index) {
      this.musicList.splice(index, 1);
      if (this.currentPlayingIndex === index) {
        this.$refs.audio.pause();
        this.currentPlayingIndex = null;
        this.isPaused = true;
      }
    },
    formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60).toString().padStart(2, '0');
      return `${minutes}:${seconds}`;
    },
    onMusicEnd() {
      this.isPaused = true;
      this.currentPlayingIndex = null;
    },
  },
};
</script>

<style scoped>
audio {
  display: none;
}
</style>
