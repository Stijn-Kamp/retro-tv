<template>
  <div class="next-up" v-if="song">
    <p class="label">{{ label }}</p>

    <div class="details">
      <p class="artist">{{ song.artist }}</p>
      <p class="title">{{ song.title }}</p>
    </div>
  </div>

    <div class="thumbnail-wrapper" :class="{ visible: showThumb && !!song.cover }">
      <img
        v-if="song.cover"
        :src="song.cover"
        :alt="song.title"
        class="thumbnail"
      />
      <div v-else class="thumbnail-placeholder" />
    </div>

</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  song:      { type: Object,  default: null },
  label:     { type: String,  default: 'Next' },
  showThumb: { type: Boolean, default: false },
})

const thumbVisible = ref(false)

function onLoad() {
  thumbVisible.value = false
  requestAnimationFrame(() => {
    requestAnimationFrame(() => { thumbVisible.value = true })
  })
}

watch(() => props.song, () => {
  thumbVisible.value = false
})
</script>

<style scoped>
.next-up {
  padding: 16px 20px 8px;
  flex-shrink: 0;
  gap: .5em;
  display: flex;
  flex-direction: column;
}

p { margin: 0; }

/* ── thumbnail ── */
.thumbnail-wrapper {
  width: 100%;
  overflow: hidden;

  max-height: 0;
  opacity: 0;
  transform: translateY(-8px);

 transition:
  max-height 1800ms cubic-bezier(0.22, 1, 0.36, 1),
  opacity    1100ms ease 250ms,
  transform  1800ms cubic-bezier(0.22, 1, 0.36, 1);;
}

.thumbnail-wrapper.visible {
  max-height: 600px;
  opacity: 1;
  transform: translateY(0);
}

.thumbnail,
.thumbnail-placeholder {
  display: block;
  width: 100%;
  height: auto;
}

.thumbnail-placeholder {
  aspect-ratio: 1 / 1;
  background: color-mix(in srgb, var(--primary-color, #00ffff) 12%, transparent);
}
</style>