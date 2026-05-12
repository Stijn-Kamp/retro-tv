import messagesRaw from './messages.csv?raw'

function parseCSV(csv) {
  const lines = csv.trim().split('\n')

  return lines.slice(1).map(line => {
    const [title, message] = line.split(',')

    return {
      title: title?.trim() ?? '',
      message: message?.trim() ?? ''
    }
  })
}

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

export const messages = shuffle(parseCSV(messagesRaw))