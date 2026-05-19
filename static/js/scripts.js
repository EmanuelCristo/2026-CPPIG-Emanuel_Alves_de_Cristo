 function updateTime() {

  const timeElement = document.getElementById('relogio');
  const dataElement = document.getElementById('data');

  const now = new Date();

  const today = now.toLocaleDateString('pt-BR');
  dataElement.textContent = today;

  const hours = now.getHours().toString().padStart(2, '0');
  const minutes = now.getMinutes().toString().padStart(2, '0');
  const seconds = now.getSeconds().toString().padStart(2, '0');
  const timeString = `${hours}:${minutes}:${seconds}`;
  timeElement.textContent = timeString;
}

setInterval(updateTime, 1000);
updateTime();

