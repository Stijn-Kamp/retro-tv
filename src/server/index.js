import express from 'express'
import Database from 'better-sqlite3'
import { glob } from 'glob'
import path from 'path'
import { fileURLToPath } from 'url'
import cors from 'cors'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const app = express()

// ✅ enable CORS (allow all origins)
app.use(cors())

// Find all playlist.db files under media/songs
function loadAllSongs() {
  const dbFiles = glob.sync('../../media/songs/**/playlist.db', { cwd: __dirname })
  const songs = []

  for (const dbFile of dbFiles) {
    const db = new Database(path.resolve(__dirname, dbFile), { readonly: true })
    const rows = db.prepare('SELECT * FROM songs').all()
    songs.push(...rows)
    db.close()
  }

  return songs
}

// Ping endpoint
app.get('/api/ping', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: Date.now()
  })
})

app.get('/api/songs', (req, res) => {
  try {
    const songs = loadAllSongs()
    res.json(songs)
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.use('/media', express.static(path.resolve(__dirname, '../media')))

app.listen(3001, () => console.log('API running on http://localhost:3001'))