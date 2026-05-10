<script setup>
import { ref } from 'vue'
import VideoPlayer from './components/VideoPlayer.vue'
import ChannelLogo from './components/ChannelLogo.vue'
import BottomBar from './components/BottomBar.vue'
import Sidebar from './components/SideBar.vue'
import PlayerControls from './components/PlayerControls.vue'
import { usePlaylist } from './playlist.js'

const { queue, playNext, playPrev, reshuffle } = usePlaylist()
const paused = ref(false)

function togglePause() {
  paused.value = !paused.value
}
</script>

<template>
  <div class="tv-app">
    <VideoPlayer :src="queue[0].src" :paused="paused" @ended="playNext" />
    <ChannelLogo />
    <PlayerControls :paused="paused" @prev="playPrev" @toggle-pause="togglePause" @skip="playNext" @reshuffle="reshuffle" />
    <Sidebar :current="queue[0]" :next="queue[1]" />
    <BottomBar
      :items="[
        { title: 'NEWS', message: 'Wereldgozers gaan op vakantie' },
        { title: 'NEWS', message: 'Robs auto is stuk' },
        { title: 'NEWS', message: 'Het wordt weer gezellig' }
      ]"
    />
  </div>
</template>

<style>
.tv-app {
  position: fixed;
  inset: 0;
  z-index: 1;
}
</style>