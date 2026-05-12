<template>
  <div class="right-sidebar overlay-bar">
    <Transition name="slide-fade" mode="out-in">
      <div :key="showPlaylist ? 'playlist' : 'info'" class="content-wrapper">

        <div v-if="!showPlaylist" class="content">
          <NowPlaying :song="current" />
          <Transition name="fade" mode="out-in">
            <div :key="showNext ? 'visible' : 'hidden'" class="next-block">
              <template v-if="showNext">
                <NextUp :song="next" label="Next" />
                <NextUp :song="later" label="Later" />
              </template>
            </div>
          </Transition>
          <Thumbnail class="thumbnail-wrapper" :src="current?.thumbnail" />
        </div>

        <Playlist v-else :queue="queue" />

      </div>
    </Transition>
  </div>
</template>

<script setup>
  import { computed, ref, onMounted, onUnmounted  } from 'vue'
  import Thumbnail from './Thumbnail.vue'
  import NextUp from './NextUp.vue'
  import NowPlaying from './NowPlaying.vue'
  import Playlist from './Playlist.vue'
  
  const showPlaylist = ref(false)
  const showNext = ref(true)
  
  let playlistInterval
  let nextInterval

  onMounted(() => {
    playlistInterval = setInterval(() => {
      showPlaylist.value = !showPlaylist.value
    }, 15000)

    // nextInterval = setInterval(() => {
    //   showNext.value = !showNext.value
    // }, 5000)
  })

  onUnmounted(() => {
    clearInterval(playlistInterval)
    clearInterval(nextInterval)
  })

  const props = defineProps({
    queue: {
      type: Array,
      default: () => []
    }
  })

  const current = computed(() => {
    return props.queue?.[0] ?? null
  })

  const next = computed(() => {
    return props.queue?.[1] ?? null
  })

  const later = computed(() => {
    return props.queue?.[2] ?? null
  })
</script>

<style scoped>
.right-sidebar {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 400px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  padding-top: 1em;
  font-size: 2em;
}

.content {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.thumbnail-wrapper {
  margin-top: auto;
}
</style>