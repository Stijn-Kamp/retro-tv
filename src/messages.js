import messagesRaw from './messages.csv?raw'

function parseCSV(csv) {
  const lines = csv.trim().split('\n')

  // assume: title,message
  return lines.slice(1).map(line => {
    const [title, message] = line.split(',')

    return {
      title: title?.trim() ?? '',
      message: message?.trim() ?? ''
    }
  })
}

export const messages = parseCSV(messagesRaw)