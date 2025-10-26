document.addEventListener('DOMContentLoaded', () => {
  // highlight anchors
  if (location.hash) {
    const el = document.querySelector(location.hash);
    if (el) el.classList.add('focus-ring');
  }
});
