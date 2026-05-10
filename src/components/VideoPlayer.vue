<template>
  <div class="video-container">
    <video
      ref="video"
      class="video-element"
      :src="src"
      autoplay
      muted
      loop
      playsinline
    ></video>
  </div>
</template>

<script>
export default {
  name: "VideoPlayer",
  props: {
    src: {
      type: String,
      required: true
    }
  },
  mounted() {
    const video = this.$refs.video;
    video.play().catch(() => {
      video.muted = true;
      video.play();
    });

    document.addEventListener('click', () => {
      video.muted = false;
    }, { once: true });
  }
};
</script>

<style scoped>
.video-container {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: black;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>