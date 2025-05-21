import streamlit as st

html_code = """
<style>
  .game-container{
      max-width:350px;
      margin:0 auto;
      display:flex;
      flex-direction:column;
      align-items:center;
      font-family:sans-serif;
  }
  .status{
      margin-bottom:0.5rem;
      font-weight:bold;
  }
  #board{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:8px;
      width:100%;
  }
  .cell{
      background:#fff;
      border-radius:12px;
      box-shadow:0 2px 5px rgba(0,0,0,0.2);
      aspect-ratio:1;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:2rem;
      cursor:pointer;
      transition:transform .2s, box-shadow .2s;
  }
  .cell:hover{
      box-shadow:0 0 15px rgba(0,123,255,0.6);
      transform:scale(1.05);
  }
  .cell.win{
      background:#fffb91;
      box-shadow:0 0 15px rgba(255,215,0,0.8);
  }
  #reset{
      margin-top:1rem;
      padding:.5rem 1.2rem;
      border:none;
      border-radius:8px;
      background:#0d6efd;
      color:#fff;
      font-weight:bold;
      cursor:pointer;
      box-shadow:0 2px 5px rgba(0,0,0,0.2);
      transition:background .3s, transform .2s;
  }
  #reset:hover{background:#0b5ed7;}
</style>

<div class="game-container">
  <div class="status"></div>
  <div id="board">
    <div class="cell" data-cell="0"></div>
    <div class="cell" data-cell="1"></div>
    <div class="cell" data-cell="2"></div>
    <div class="cell" data-cell="3"></div>
    <div class="cell" data-cell="4"></div>
    <div class="cell" data-cell="5"></div>
    <div class="cell" data-cell="6"></div>
    <div class="cell" data-cell="7"></div>
    <div class="cell" data-cell="8"></div>
  </div>
  <button id="reset">Reset</button>
</div>

<script>
  const board = Array(9).fill('');
  const cells = document.querySelectorAll('.cell');
  const status = document.querySelector('.status');
  let currentPlayer = 'X';
  const winningCombos = [
      [0,1,2],[3,4,5],[6,7,8],
      [0,3,6],[1,4,7],[2,5,8],
      [0,4,8],[2,4,6]
  ];

  function checkWin(){
      for (const combo of winningCombos){
          const [a,b,c] = combo;
          if(board[a] && board[a]===board[b] && board[b]===board[c]){
              combo.forEach(i => cells[i].classList.add('win'));
              status.textContent = `Player ${board[a]} wins!`;
              cells.forEach(cell => cell.removeEventListener('click', handleClick));
              return true;
          }
      }
      if(board.every(Boolean)) status.textContent = 'Draw!';
      return false;
  }

  function handleClick(e){
      const idx = +e.target.dataset.cell;
      if(board[idx]) return;
      board[idx] = currentPlayer;
      e.target.textContent = currentPlayer;
      e.target.classList.add('filled');
      if(!checkWin()){
          currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
          status.textContent = `Player ${currentPlayer}'s turn`;
      }
  }

  cells.forEach(cell => cell.addEventListener('click', handleClick));
  status.textContent = `Player ${currentPlayer}'s turn`;

  document.getElementById('reset').addEventListener('click', ()=>{
      board.fill('');
      cells.forEach(c => {
          c.textContent = '';
          c.classList.remove('filled','win');
          c.addEventListener('click', handleClick);
      });
      currentPlayer = 'X';
      status.textContent = `Player ${currentPlayer}'s turn`;
  });

  /* Optional: to initialize from Python, you could pass a JSON string
     and replace `board` with it:
     const board = JSON.parse("{{ board_state_json }}");
  */
</script>
"""

st.components.v1.html(html_code, height=400)
