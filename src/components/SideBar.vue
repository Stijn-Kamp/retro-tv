<template>
  <div class="right-sidebar overlay-bar">
    <NowPlaying
      :artist="current?.artist"
      :song="current?.title"
      :album="current?.album"
      :year="current?.year"
    />
    <NextUp :song="next?.filename" />
    <div class="thumbnail-wrapper">
      <Thumbnail :src="current?.thumbnail" />
    </div>
  </div>
</template>

<script setup>
  import { computed } from 'vue'

  import Thumbnail from './Thumbnail.vue'
  import NextUp from './NextUp.vue'
  import NowPlaying from './NowPlaying.vue'

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

.thumbnail-wrapper {
  margin-top: auto;
}
</style>