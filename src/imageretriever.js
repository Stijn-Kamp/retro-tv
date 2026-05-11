import { ref, computed, watch } from 'vue'

// change this path to whatever folder you want
const imageModules = import.meta.glob(
  '../media/images/**/*.{jpg,jpeg,png}',
  { eager: true }
)

// convert module map → flat array of URLs
const images = Object.values(imageModules).map(m => m.default)

function getRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)]
}

export function useRandomBackground(currentSong) {
  const currentImage = ref(getRandom(images))

  function pickNewImage() {
    if (images.length === 0) return
    currentImage.value = getRandom(images)
  }

  // every time song changes → new image
  watch(currentSong, () => {
    pickNewImage()
  }, { immediate: true })

  return {
    currentImage,
  }
}