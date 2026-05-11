import { ref, computed, watch } from 'vue'

const videoModules = import.meta.glob(
  '../media/songs/**/*.mp4',
  { eager: true }
)

const metadataModules = import.meta.glob(
  '../media/songs/**/metadata.json',
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

function buildSongs() {
  return Object.keys(videoModules).map(videoKey => {
    const metaKey = videoKey.replace(/\/[^/]+\.mp4$/, '/metadata.json')
    const meta = metadataModules[metaKey]?.default ?? metadataModules[metaKey] ?? null

    const videoSrc = videoModules[videoKey].default
    const coverSrc = videoSrc.replace(/\/[^/]+\.mp4(\?.*)?$/, '/cover.jpg')

    if (meta) {
      return {
        src: videoSrc,
        cover: coverSrc,
        title: meta.title ?? '',
        artist: meta.artist ?? '',
        album: meta.album ?? '',
        date: meta.date ?? '',
        year: meta.year ?? '',
        duration: meta.duration_str ?? '',
        release_id: meta.release_id ?? '',
      }
    }

    const filename = videoKey.split('/').pop().replace('.mp4', '')
    const dashIndex = filename.indexOf(' - ')
    const artist = dashIndex !== -1 ? filename.slice(0, dashIndex).trim() : filename
    const title = dashIndex !== -1
      ? filename.slice(dashIndex + 3)
          .replace(/\s*\(official.*?\)/i, '')
          .replace(/\s*\[official.*?\]/i, '')
          .trim()
      : filename

    return {
      src: videoSrc,
      cover: coverSrc,
      title,
      artist,
      album: '',
      date: '',
      year: '',
      duration: '',
      release_id: '',
    }
  })
}

const allSongs = buildSongs()

export function usePlaylist() {
  const playlist = ref(shuffle(allSongs))
  const currentIndex = ref(0)

  const showTitleBar = ref(true)
  const showImageViewer = ref(true)
  const showSidebar = ref(false)
  const showBottomBar = ref(false)

  const timers = []

  function clearSchedule() {
    timers.forEach(t => clearTimeout(t))
    timers.length = 0
  }

  function runSchedule() {
    clearSchedule()

    showTitleBar.value = true
    showImageViewer.value = true
    showSidebar.value = false
    showBottomBar.value = false

    const schedule = [
      {
        at: 5000,
        run: () => (showTitleBar.value = false)
      },
      {
        at: 10000,
        run: () => (showImageViewer.value = false)
      },
      {
        at: 20000,
        run: () => (showSidebar.value = true)
      },
      {
        at: 20000,
        run: () => (showBottomBar.value = true)
      }
    ]

    schedule.forEach(step => {
      const t = setTimeout(step.run, step.at)
      timers.push(t)
    })
  }

  const currentSong = computed(() => playlist.value[currentIndex.value])

  const nextSong = computed(() => {
    if (!playlist.value.length) return null
    return playlist.value[(currentIndex.value + 1) % playlist.value.length]
  })

  watch(currentSong, () => {
    runSchedule()
  }, { immediate: true })

  function playNext() {
    currentIndex.value = (currentIndex.value + 1) % playlist.value.length
  }

  function playPrev() {
    currentIndex.value =
      (currentIndex.value - 1 + playlist.value.length) % playlist.value.length
  }

  function reshuffle() {
    playlist.value = shuffle(allSongs)
    currentIndex.value = 0
  }

  const queue = computed(() => {
    const rest = playlist.value.slice(currentIndex.value)
    return rest.length ? rest : playlist.value
  })

  return {
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
  }
}