fetch("dados.txt")
  .then(resposta => resposta.text())
  .then(texto => document.querySelector("#resultado").textContent = texto);
