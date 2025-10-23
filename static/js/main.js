function copyJSON() {
  const pre = document.getElementById('parsed-json');
  if (!pre) return;
  const text = pre.innerText;
  navigator.clipboard.writeText(text).then(() => {
    alert('JSON copied to clipboard');
  });
}

function downloadJSON() {
  const pre = document.getElementById('parsed-json');
  if (!pre) return;
  const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(pre.innerText);
  const a = document.createElement('a');
  a.href = dataStr;
  a.download = 'parsed.json';
  document.body.appendChild(a);
  a.click();
  a.remove();
}

document.addEventListener('DOMContentLoaded', () => {
  const chips = document.querySelectorAll('.issuer-chip');
  chips.forEach(c => c.addEventListener('click', () => {
    const sel = document.getElementById('issuer');
    if (sel) sel.value = c.dataset.iss;
    c.classList.add('selected');
    setTimeout(() => c.classList.remove('selected'), 600);
  }));
});
