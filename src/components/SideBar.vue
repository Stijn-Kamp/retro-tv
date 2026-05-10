<template>
  <div class="right-sidebar overlay-bar">
    <Thumbnail src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.albumoftheyear.org%2Falbum%2Fthe-eminem-show-1.jpg&f=1&nofb=1&ipt=573a258917064c0178d4d9ef4ec7c2278f3290f00b3438d9877e7a10d7a0dfc9" />
    <NowPlaying
      artist="Eminem"
      song="Without me"
      album="The Slim Shady Show"
      year="02"
    />
    <NextUp song="Bruno Mars - Grenade" />
  </div>
</template>

<script setup>
import Thumbnail from './Thumbnail.vue'
import NextUp from './NextUp.vue'
import NowPlaying from './NowPlaying.vue'
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