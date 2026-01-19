function pad2(n) {
  return String(n).padStart(2, '0')
}

function localPartsFromDate(d) {
  return {
    y: d.getFullYear(),
    m: pad2(d.getMonth() + 1),
    day: pad2(d.getDate()),
    hh: pad2(d.getHours()),
    mm: pad2(d.getMinutes()),
    ss: pad2(d.getSeconds()),
  }
}

export function formatIsoHuman(iso, opts = {}) {
  if (!iso) return ''
  const d = new Date(String(iso))
  if (Number.isNaN(d.getTime())) return String(iso)

  const {
    locale = 'ru-RU',
    withSeconds = false,
    withDate = true,
    withTime = true,
  } = opts

  const formatOptions = {}

  if (withDate) {
    formatOptions.year = 'numeric'
    formatOptions.month = '2-digit'
    formatOptions.day = '2-digit'
  }
  if (withTime) {
    formatOptions.hour = '2-digit'
    formatOptions.minute = '2-digit'
    if (withSeconds) formatOptions.second = '2-digit'
  }
  formatOptions.timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone
  return new Intl.DateTimeFormat(locale, formatOptions).format(d)
}

export function formatIsoDate(iso, opts = {}) {
  return formatIsoHuman(iso, { ...opts, withTime: false, withDate: true })
}

export function formatIsoTime(iso, opts = {}) {
  return formatIsoHuman(iso, { ...opts, withTime: true, withDate: false })
}

export function toIsoFromDt(dt) {
  if (!dt?.date) return null
  const time = dt?.time || '00:00'
  const [y, m, day] = dt.date.split('-').map(Number)
  const [hh, mm] = time.split(':').map(Number)
  const d = new Date(y, (m || 1) - 1, day || 1, hh || 0, mm || 0, 0)
  const offMin = -d.getTimezoneOffset()
  const sign = offMin >= 0 ? '+' : '-'
  const abs = Math.abs(offMin)
  const offH = pad2(Math.floor(abs / 60))
  const offM = pad2(abs % 60)

  const p = localPartsFromDate(d)
  return `${p.y}-${p.m}-${p.day}T${p.hh}:${p.mm}:00${sign}${offH}:${offM}`
}

export function splitIso(iso) {
  if (!iso) return { date: '', time: '' }
  const d = new Date(String(iso))
  if (Number.isNaN(d.getTime())) return { date: '', time: '' }

  const p = localPartsFromDate(d)
  return { date: `${p.y}-${p.m}-${p.day}`, time: `${p.hh}:${p.mm}` }
}
