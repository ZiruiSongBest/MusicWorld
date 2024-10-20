<template>
  <div class="library-container min-h-screen p-6 bg-gray-50 w-full max-w-5xl mx-auto">
    <h1 class="text-4xl font-bold mb-6 text-center">Generated Music Library</h1>

    <!-- Music List -->
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
            <audio :src="music.url" controls></audio> <!-- 播放音频 -->
          </div>
        </div>

        <!-- Delete Button -->
        <button 
          @click="removeMusic(index)" 
          class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors">
          Delete
        </button>
      </div>
    </div>

    <!-- No Music Message -->
    <div v-else class="text-center text-gray-600 mt-12">
      <p>No generated music available. Please generate some music first!</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      musicList: [], // 用于存储音乐列表
    };
  },
  methods: {
    removeMusic(index) {
      this.musicList.splice(index, 1); // 从列表中删除音乐
    },
    addMusicToLibrary(musicData) {
      this.musicList.push(musicData); // 将新生成的音乐数据添加到音乐列表中
    }
  },
  created() {
    // 从路由参数中接收音乐数据
    const musicData = this.$route.params.musicData;
    if (musicData) {
      this.addMusicToLibrary(musicData); // 添加音乐到列表
    }
  }
};
</script>

<style scoped>
.library-container {
  padding: 2rem;
}
</style>
