import { ref, computed, watch } from 'vue'

const videoModules = import.meta.glob('../media/songs/**/*.mp4', { eager: true })
const metadataModules = import.meta.glob('../media/songs/**/metadata.json', { eager: true })

// --- Helpers ---

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function unwrapMeta(module) {
  const raw = module?.default ?? module ?? {}
  if (!raw || typeof raw !== 'object') return null
  if (raw.title || raw.artist || raw.album) return raw
  return Object.values(raw)[0] ?? null
}

function findMeta(videoKey) {
  const folderName = videoKey.split('/').slice(0, -1).pop()
  const entry = Object.entries(metadataModules).find(([k]) => k.includes(folderName))
  return entry ? unwrapMeta(entry[1]) : null
}

function songFromMeta(videoSrc, coverSrc, meta) {
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

function songFromFilename(videoSrc, coverSrc, videoKey) {
  const filename = videoKey.split('/').pop().replace('.mp4', '')
  const dash = filename.indexOf(' - ')
  const artist = dash !== -1 ? filename.slice(0, dash).trim() : filename
  const title = dash !== -1
    ? filename.slice(dash + 3)
        .replace(/\s*\(official.*?\)/i, '')
        .replace(/\s*\[official.*?\]/i, '')
        .trim()
    : filename
  return { src: videoSrc, cover: coverSrc, title, artist, album: '', date: '', year: '', duration: '', release_id: '' }
}

function buildSongs() {
  return Object.entries(videoModules).map(([videoKey, mod]) => {
    const videoSrc = mod.default
    const coverSrc = videoSrc.replace(/\/[^/]+\.mp4(\?.*)?$/, '/cover.jpg')
    const meta = findMeta(videoKey)
    return meta
      ? songFromMeta(videoSrc, coverSrc, meta)
      : songFromFilename(videoSrc, coverSrc, videoKey)
  })
}

// --- Schedule ---

const SCHEDULE = [
  { at: 5000,  key: 'showTitleBar',    value: false },
  { at: 10000, key: 'showImageViewer', value: false },
  { at: 20000, key: 'showSidebar',     value: true  },
  { at: 20000, key: 'showBottomBar',   value: true  },
]

// --- Playlist ---

const allSongs = buildSongs()

export function usePlaylist() {
  const playlist = ref(shuffle(allSongs))
  const currentIndex = ref(0)

  const showTitleBar    = ref(true)
  const showImageViewer = ref(true)
  const showSidebar     = ref(false)
  const showBottomBar   = ref(false)

  const visibility = { showTitleBar, showImageViewer, showSidebar, showBottomBar }

  const timers = []

  function runSchedule() {
    timers.forEach(clearTimeout)
    timers.length = 0

    showTitleBar.value    = true
    showImageViewer.value = true
    showSidebar.value     = false
    showBottomBar.value   = false

    SCHEDULE.forEach(({ at, key, value }) => {
      timers.push(setTimeout(() => { visibility[key].value = value }, at))
    })
  }

  const currentSong = computed(() => playlist.value[currentIndex.value])
  const nextSong    = computed(() => playlist.value[(currentIndex.value + 1) % playlist.value.length] ?? null)

  watch(currentSong, runSchedule, { immediate: true })

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

  return {
    queue,
    currentSong,
    nextSong,
    playNext,
    playPrev,
    reshuffle,
    ...visibility,
  }
}