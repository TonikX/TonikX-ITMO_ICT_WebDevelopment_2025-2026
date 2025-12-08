export function getAgeFromDate(birthDate) {
  if (!birthDate) {
    return "";
  }

  const birth = new Date(birthDate);
  const today = new Date();

  let years = today.getFullYear() - birth.getFullYear();
  let months = today.getMonth() - birth.getMonth();
  let days = today.getDate() - birth.getDate();

  if (days < 0) {
    months -= 1;
    const prevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
    days += prevMonth.getDate();
  }

  if (months < 0) {
    years -= 1;
    months += 12;
  }

  const parts = [];

  if (years > 0) {
    parts.push(`${years} г.`);
  }

  if (months > 0) {
    parts.push(`${months} м.`);
  }

  if (days > 0) {
    parts.push(`${days} д.`);
  }

  return parts.join(", ");
}