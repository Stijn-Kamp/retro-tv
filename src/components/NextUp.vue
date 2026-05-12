<template>
  <div class="next-up" v-if="song">
    <p class="label">{{ label }}</p>
    <div class="details">
      <p class="artist"> {{ song.artist }} </p>
      <p class="title"> {{ song.title }} </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  song: {
    type: Object,
    default: null
  },
  label: {
    type: String,
    default: 'Next'
  }
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

p {
  margin: 0px;
}

</style>