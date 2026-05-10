<script setup>
import VideoPlayer from './components/VideoPlayer.vue'
import ChannelLogo from './components/ChannelLogo.vue'
import BottomBar from './components/BottomBar.vue'
import Sidebar from './components/SideBar.vue'
import pumpIt from './videos/The Black Eyed Peas - Pump It (Official Music Video).mp4'
</script>

<template>
  <div class="tv-app">
    <VideoPlayer :src="pumpIt" />
    <ChannelLogo />
    <Sidebar />
    <BottomBar />
  </div>
</template>

<style>
.tv-app {
  position: fixed;
  inset: 0;
  z-index: 1;
}
</style>