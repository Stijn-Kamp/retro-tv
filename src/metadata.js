import { parseFile } from 'music-metadata'
import { fileURLToPath } from 'url'
import path from 'path'
import fs from 'fs'
import { glob } from 'glob'

export default function musicMetadataPlugin() {
  return {
    name: 'music-metadata',
    async buildStart() {
      const downloadsDir = path.resolve(process.cwd(), 'downloads')
      const files = glob.sync('**/*.mp4', { cwd: downloadsDir })

      const metadata = {}
      for (const file of files) {
        const filepath = path.join(downloadsDir, file)
        try {
          const meta = await parseFile(filepath)
          const { title, artist, album, year } = meta.common
          const picture = meta.common.picture?.[0]

          metadata[file] = {
            filename: file,
            title: title || '',
            artist: artist || '',
            album: album || '',
            date: year ? String(year) : '',
            // Convert cover art to base64 data URL
            thumbnail: picture
              ? `data:${picture.format};base64,${Buffer.from(picture.data).toString('base64')}`
              : null,
          }
        } catch (e) {
          console.warn(`Failed to read metadata for ${file}:`, e.message)
        }
      }

      // Write to src/songs.json so Vite can import it
      const outPath = path.resolve(process.cwd(), 'src/songs.json')
      fs.writeFileSync(outPath, JSON.stringify(metadata, null, 2))
      console.log(`[music-metadata] wrote metadata for ${Object.keys(metadata).length} songs`)
    }
  }
}