<script setup>
import VideoPlayer from './components/VideoPlayer.vue'
import ChannelLogo from './components/ChannelLogo.vue'
import BottomBar from './components/BottomBar.vue'
import Sidebar from './components/SideBar.vue'
import pumpIt from '/home/stijn/Projects/retro-tv/downloads/Eminem - Without Me (Official Music Video).mp4'
</script>

<template>
  <div class="tv-app">
    <VideoPlayer :src="pumpIt" />
    <ChannelLogo />
    <Sidebar />
    <BottomBar title="News" message="Wereldgozers gaan op vakantie" />  
  </div>
</template>

<style>
.tv-app {
  position: fixed;
  inset: 0;
  z-index: 1;
}
</style>