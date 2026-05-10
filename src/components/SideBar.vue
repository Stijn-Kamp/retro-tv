<template>
  <div class="right-sidebar overlay-bar">
    <Thumbnail :src="current?.thumbnail" />
    <NowPlaying
      :artist="current?.artist"
      :song="current?.title"
      :album="current?.album"
      :year="current?.date"
    />
    <NextUp :song="next?.filename" />
  </div>
</template>

<script setup>
import Thumbnail from './Thumbnail.vue'
import NextUp from './NextUp.vue'
import NowPlaying from './NowPlaying.vue'

defineProps({
  current: Object,
  next: Object,
})
</script>

<style scoped>
.right-sidebar {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 280px;
  display: flex;
  flex-direction: column;
}
</style>