<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="flex justify-between items-center p-4 bg-white shadow-md">
      <div class="text-xl font-bold">Music generator</div>
      <nav class="space-x-6">
        <a href="#" class="text-gray-700">Home page</a>
        <a href="#" class="text-gray-700">Play page</a>
      </nav>
      <div class="flex items-center space-x-4">
        <img src="./assets/musichead.jpg" alt="User Avatar" class="rounded-full w-10 h-10">
        <i class="fas fa-music text-xl"></i>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 p-6 bg-gray-50 max-w-screen-lg mx-auto">
      <section class="text-center mb-8">
        <h1 class="text-5xl font-bold mb-4">Music World</h1>
        <p class="text-lg text-gray-600">
          I am an experienced web interface designer and I have designed a music generator based on your requirement.
          The generator can take three forms of input such as audio, text, and image and generate music by clicking a button.
        </p>
      </section>

      <img src="./assets/music.png">

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
            <i class="fas fa-file-audio text-4xl mb-2"></i>
            <p class="text-gray-600">Audio input</p>
          </div>
          <div class="text-center">
            <i class="fas fa-file-alt text-4xl mb-2"></i>
            <p class="text-gray-600">Text input</p>
          </div>
        </div>
      </section>

      <div class="flex justify-center">
        <img src="./assets/musicbottom.jpg" alt="Music Generation Preview" class="rounded-lg shadow-md w-full max-w-3xl">
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white p-6 shadow-inner max-w-screen-lg mx-auto">
      <div class="flex justify-between items-center">
        <p class="text-gray-600">&copy; 2024 Music World</p>
        <div class="flex space-x-4">
          <a href="#" class="text-gray-600">About us</a>
          <a href="#" class="text-gray-600">Connection method</a>
          <a href="#" class="text-gray-600">Project culture</a>
        </div>
        <div class="flex space-x-4">
          <i class="fab fa-instagram text-xl"></i>
          <i class="fab fa-twitter text-xl"></i>
          <i class="fab fa-wechat text-xl"></i>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
}
</style>
