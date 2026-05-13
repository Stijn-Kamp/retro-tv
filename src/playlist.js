import { ref, computed, watch } from 'vue'

// --- Retro color palette ---
const RETRO_COLORS = [
  '#1dddf2', 
  '#FF2052', 
  '#e2c618', 
  '#38b622',
  '#9246c5', 
  '#FF8C00', 
]

let lastColorIndex = -1

function pickRetroColor() {
  let idx
  do { idx = Math.floor(Math.random() * RETRO_COLORS.length) }
  while (idx === lastColorIndex)
  lastColorIndex = idx
  return RETRO_COLORS[idx]
}

// --- Helpers ---
function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

function rowToSong(row) {
  return {
    src:        row.video_file,
    cover:      row.cover_file ?? '',
    title:      row.title ?? '',
    artist:     row.artist ?? '',
    album:      row.album ?? '',
    date:       row.album_date ?? '',
    year:       row.year ? String(row.year).slice(-2) : '',
    duration:   row.duration_str ?? '',
    bpm:        row.bpm ?? null,
    energy:     row.energy ?? null,
    genres:     row.genres ?? '',
    camelot:    row.camelot ?? '',
    valence:    row.valence ?? null,
    spotify_id: row.spotify_track_id ?? '',
    isrc:       row.isrc ?? '',
    yt_id:      row.yt_id ?? '',
  }
}

// --- Schedule ---
const SCHEDULE = [
  { at:  7000, key: 'showTitleBar',    value: false },
  { at: 15000, key: 'showImageViewer', value: false },
  { at: 20000, key: 'showSidebar',     value: true  },
  { at: 30000, key: 'showBottomBar',   value: true  },
]

// --- Playlist ---
export function usePlaylist() {
  const playlist     = ref([])
  const currentIndex = ref(0)
  const loading      = ref(true)
  const error        = ref(null)
  const primaryColor = ref('')

  const showTitleBar    = ref(true)
  const showImageViewer = ref(true)
  const showSidebar     = ref(false)
  const showBottomBar   = ref(false)
  const visibility = { showTitleBar, showImageViewer, showSidebar, showBottomBar }

  const timers = []

  function applyPrimaryColor(color) {
    primaryColor.value = color
    document.documentElement.style.setProperty('--primary-color', color)
  }

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

    applyPrimaryColor(pickRetroColor())
  }

  fetch('http://localhost:3001/api/songs')
    .then(r => r.json())
    .then(rows => {
      playlist.value = shuffle(rows.map(rowToSong))
      loading.value  = false
    })
    .catch(e => {
      error.value   = e.message
      loading.value = false
    })

  const currentSong = computed(() => playlist.value[currentIndex.value] ?? null)
  const nextSong    = computed(() => playlist.value[(currentIndex.value + 1) % playlist.value.length] ?? null)

  watch(currentSong, (song) => { if (song) runSchedule() }, { immediate: true })

  function playNext() {
    currentIndex.value = (currentIndex.value + 1) % playlist.value.length
  }

  function playPrev() {
    currentIndex.value = (currentIndex.value - 1 + playlist.value.length) % playlist.value.length
  }

  function reshuffle() {
    playlist.value = shuffle(playlist.value)
    currentIndex.value = 0
  }

  const queue = computed(() => {
    const list = playlist.value
    const len = list.length
    const idx = currentIndex.value

    if (!len) return []

    const safeIndex = ((idx % len) + len) % len

    return [
      ...list.slice(safeIndex),
      ...list.slice(0, safeIndex)
    ]
  })

  return {
    queue,
    currentSong,
    nextSong,
    loading,
    error,
    primaryColor,
    playNext,
    playPrev,
    reshuffle,
    ...visibility,
  }
}