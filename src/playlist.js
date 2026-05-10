import { ref, computed } from 'vue'

const videoModules = import.meta.glob(
  '../downloads/**/*.mp4',
  { eager: true }
)

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function parseFilename(key) {
  const filename = key.split('/').pop().replace('.mp4', '')
  
  // Split on first " - " to get artist and rest
  const dashIndex = filename.indexOf(' - ')
  if (dashIndex === -1) {
    return { filename, src: videoModules[key].default, artist: filename, title: filename, album: '', date: '' }
  }

  const artist = filename.slice(0, dashIndex).trim()
  // Strip trailing tags like "(Official Music Video)", "(Official Video)", etc.
  const title = filename
    .slice(dashIndex + 3)
    .replace(/\s*\(official.*?\)/i, '')
    .replace(/\s*\[official.*?\]/i, '')
    .trim()

  return {
    filename,
    src: videoModules[key].default,
    artist,
    title,
    album: '',
    date: '',
  }
}

const allSongs = Object.keys(videoModules).map(parseFilename)

export function usePlaylist() {
  const playlist = ref(shuffle(allSongs))
  const currentIndex = ref(0)

  const currentSong = computed(() => playlist.value[currentIndex.value])
  const nextSong = computed(() => playlist.value[(currentIndex.value + 1) % playlist.value.length])

  function playNext() {
    currentIndex.value = (currentIndex.value + 1) % playlist.value.length
  }

  function playPrev() {
    currentIndex.value = (currentIndex.value - 1 + playlist.value.length) % playlist.value.length
  }

  function reshuffle() {
    playlist.value = shuffle(allSongs)
    currentIndex.value = 0
  }

  const queue = computed(() => {
    const rest = playlist.value.slice(currentIndex.value)
    return rest.length ? rest : playlist.value
  })

  return { queue, playNext, playPrev, reshuffle }
}