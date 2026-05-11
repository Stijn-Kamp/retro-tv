<template>
  <div class="title-bar">
    <div class="grid">

      <span class="label artist-label">Artist</span>
      <span class="label year-label">Year</span>
      <span class="value artist-value">{{ song?.artist }}</span>
      <span class="value year-value">'{{ song?.year }}</span>

      <span class="label song-label">Song</span>
      <span class="label length-label">Length</span>
      <span class="value song-value">{{ song?.title }}</span>
      <span class="value length-value">{{ song?.duration }}</span>

      <span class="label album-label">Album</span>
      <span class="value album-value">{{ song?.album }}</span>

    </div>
  </div>
</template>

<script setup>
defineProps({
  song: Object
})
</script>

<style scoped>
.title-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 50vh;    
    background: linear-gradient(
        to bottom,
        transparent 0%,
        var(--overlay-bg) 10%
    );  
    display: flex;
    align-items: flex-end;
    padding: 0 128px 16px;
    z-index: 20;
}

.grid {
    display: grid;
    grid-template-columns: 1fr auto;
    grid-template-rows: auto auto auto;
    column-gap: 32px;
    row-gap: 2px;
    width: 100%;
}

.value {
    font-size: 3rem;
    font-weight: 600;
    color: white;
    line-height: 1.2;
}

/* row 1 */
.artist-label { grid-column: 1; grid-row: 1; }
.year-label   { grid-column: 2; grid-row: 1; text-align: right; }
.artist-value { grid-column: 1; grid-row: 2; font-size: 6em;}
.year-value   { grid-column: 2; grid-row: 2; text-align: right; font-size: 6em; }

/* row 2 */
.song-label   { grid-column: 1; grid-row: 3; margin-top: 6px; }
.length-label { grid-column: 2; grid-row: 3; text-align: right; margin-top: 6px; }
.song-value   { grid-column: 1; grid-row: 4; }
.length-value { grid-column: 2; grid-row: 4; text-align: right; }

/* row 3 */
.album-label  { grid-column: 1 / -1; grid-row: 5; margin-top: 6px; }
.album-value  { grid-column: 1 / -1; grid-row: 6; }
</style>