<script setup>
import { ref } from 'vue'
import InfoComponent from './components/InfoComponent.vue';
import VideoPlayer from './components/VideoPlayer.vue'
import ImageViewer from './components/ImageViewer.vue'
import TitleBar from './components/TitleBar.vue'
import ChannelLogo from './components/ChannelLogo.vue'
import BottomBar from './components/BottomBar.vue'
import Sidebar from './components/SideBar.vue'
import PlayerControls from './components/PlayerControls.vue'
import { usePlaylist } from './playlist.js'
import { useRandomBackground } from './imageretriever.js'
import { messages } from './messages.js'

const {
    queue,
    currentSong,
    nextSong,
    playNext,
    playPrev,
    reshuffle,
    showTitleBar,
    showImageViewer,
    showSidebar,
    showBottomBar
  } = usePlaylist()

const { currentImage } = useRandomBackground(currentSong)

const paused = ref(false)
const controlsVisible = ref(false)
let hideTimer = null

function onMouseMove() {
  controlsVisible.value = true
  clearTimeout(hideTimer)
  hideTimer = setTimeout(() => {
    controlsVisible.value = false
  }, 3000)
}

function togglePause() {
  paused.value = !paused.value
}
</script>

<template>
  <div v-if="queue.length" class="tv-app" @mousemove="onMouseMove">
    <VideoPlayer :src="currentSong.src" :paused="paused" @ended="playNext" />
    <ChannelLogo />
    <InfoComponent />
    <Transition name="fade">
      <PlayerControls
        v-if="controlsVisible"
        :paused="paused"
        @prev="playPrev"
        @toggle-pause="togglePause"
        @skip="playNext"
        @reshuffle="reshuffle"
      />
    </Transition>
    <Transition name="side">
      <Sidebar
        v-if="showSidebar"
        :queue="queue"
      />
    </Transition>
    <Transition name="bottom">
      <BottomBar
        v-if="showBottomBar"
        :items="messages"
      />
    </Transition>
    <Transition name="bottom">
      <TitleBar v-if="showTitleBar" :song="currentSong" />
    </Transition>

    <Transition name="fade">
      <ImageViewer
        v-if="showImageViewer"
        :src="currentImage"
      />
    </Transition>
  </div>
</template>

<style>
.tv-app {
  position: fixed;
  inset: 0;
  z-index: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>