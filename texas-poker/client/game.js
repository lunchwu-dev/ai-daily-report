// Texas Poker Client
const socket = io();

let currentPlayer = null;
let currentTable = null;
let gameState = null;

const loginScreen = document.getElementById('loginScreen');
const lobbyScreen = document.getElementById('lobbyScreen');
const gameScreen = document.getElementById('gameScreen');
const joinModal = document.getElementById('joinModal');

function showScreen(screen) {
    loginScreen.style.display = 'none';
    lobbyScreen.style.display = 'none';
    gameScreen.style.display = 'none';
    screen.style.display = screen === loginScreen ? 'flex' : 'block';
}

function createTable() {
    const playerName = document.getElementById('playerName').value.trim();
    if (!playerName) { alert('请输入昵称'); return; }
    socket.emit('create-table', { tableName: playerName + ' 的牌桌', playerName, maxPlayers: 6 });
}

function showJoinForm() {
    const playerName = document.getElementById('playerName').value.trim();
    if (!playerName) { alert('请输入昵称'); return; }
    joinModal.classList.add('active');
}

function hideJoinForm() { joinModal.classList.remove('active'); }

function joinTable() {
    const playerName = document.getElementById('playerName').value.trim();
    const tableId = document.getElementById('tableId').value.trim();
    if (!tableId) { alert('请输入牌桌ID'); return; }
    socket.emit('join-table', { tableId, playerName });
}

socket.on('table-created', (data) => {
    currentPlayer = { id: data.playerId, name: document.getElementById('playerName').value.trim() };
    currentTable = data.table;
    enterLobby();
});

socket.on('joined-table', (data) => {
    currentPlayer = { id: data.playerId, name: document.getElementById('playerName').value.trim() };
    currentTable = data.table;
    enterLobby();
});

socket.on('game-started', (state) => { gameState = state; showScreen(gameScreen); renderGame(); });
socket.on('game-update', (state) => { gameState = state; renderGame(); });
socket.on('hand-ended', (data) => { setTimeout(() => alert(`获胜者: ${data.winners.map(w=>w.name).join(', ')}，赢得 ${data.pot} 筹码`), 500); });
socket.on('player-joined', (data) => { if (currentTable?.id === data.table.id) { currentTable = data.table; updateLobby(); } });
socket.on('error', (msg) => alert('错误: ' + msg));

function enterLobby() {
    showScreen(lobbyScreen);
    document.getElementById('lobbyPlayerName').textContent = currentPlayer.name;
    document.getElementById('lobbyAvatar').textContent = currentPlayer.name[0].toUpperCase();
    updateLobby();
}

function updateLobby() {
    document.getElementById('tableList').innerHTML = `
        <div class="table-card" style="border: 2px solid #4CAF50;">
            <div class="table-header">
                <div class="table-name">${currentTable.name}</div>
                <div class="table-status ${currentTable.state !== 'waiting' ? 'playing' : ''}">${currentTable.state === 'waiting' ? '等待中' : '游戏中'}</div>
            </div>
            <div class="table-info">
                <span>👥 ${currentTable.playerCount}/${currentTable.maxPlayers}</span>
                <span>🆔 ${currentTable.id}</span>
            </div>
            <div style="margin-top: 15px;">
                <button class="btn btn-primary" onclick="startGame()" ${currentTable.state !== 'waiting' ? 'disabled' : ''}>${currentTable.state === 'waiting' ? '开始游戏' : '游戏进行中'}</button>
                <button class="btn btn-secondary" onclick="copyTableId()">复制邀请链接</button>
            </div>
        </div>`;
}

function startGame() { socket.emit('start-game'); }

function copyTableId() {
    const url = `${window.location.origin}?table=${currentTable.id}`;
    navigator.clipboard.writeText(url).then(() => alert('邀请链接已复制: ' + url));
}

function renderGame() {
    if (!gameState) return;
    document.getElementById('pot').textContent = `底池: ${gameState.pot}`;
    document.getElementById('communityCards').innerHTML = gameState.communityCards.map(card => `
        <div class="card ${card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'}">
            <div class="suit">${card.suit}</div>
            <div class="rank">${card.rank}</div>
        </div>`).join('');
    renderPlayers();
    updateActionButtons();
}

function renderPlayers() {
    const positions = [
        { bottom: '5%', left: '50%', transform: 'translateX(-50%)' },
        { bottom: '20%', left: '10%' }, { top: '20%', left: '10%' },
        { top: '5%', left: '50%', transform: 'translateX(-50%)' },
        { top: '20%', right: '10%' }, { bottom: '20%', right: '10%' }
    ];
    document.getElementById('playerSeats').innerHTML = gameState.players.map((player, i) => {
        const pos = positions[i % 6];
        const isMe = player.id === gameState.playerId || (currentPlayer && player.id === currentPlayer.id);
        const style = Object.entries(pos).map(([k,v]) => `${k}:${v}`).join(';');
        return `
            <div class="player-seat ${player.isTurn ? 'active' : ''} ${player.isDealer ? 'dealer' : ''}" style="${style}">
                ${player.currentBet > 0 ? `<div class="player-bet">${player.currentBet}</div>` : ''}
                <div class="player-avatar">${player.name[0].toUpperCase()}</div>
                <div class="player-name">${player.name} ${isMe ? '(我)' : ''}</div>
                <div class="player-chips">💰 ${player.chips}</div>
                ${isMe && gameState.myHand ? `
                    <div style="display: flex; gap: 5px; justify-content: center; margin-top: 5px;">
                        ${gameState.myHand.map(card => `
                            <div class="card ${card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'}" style="width: 30px; height: 42px; font-size: 10px;">
                                <div class="suit" style="font-size: 14px;">${card.suit}</div>
                                <div class="rank">${card.rank}</div>
                            </div>`).join('')}
                    </div>` : ''}
            </div>`;
    }).join('');
}

function updateActionButtons() {
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.disabled = !gameState.isMyTurn;
        btn.style.opacity = gameState.isMyTurn ? '1' : '0.5';
    });
}

function fold() { socket.emit('player-action', { action: 'fold' }); }
function check() { socket.emit('player-action', { action: 'check' }); }
function call() { socket.emit('player-action', { action: 'call' }); }
function raise() {
    const amount = prompt('请输入加注金额:', '40');
    if (amount) socket.emit('player-action', { action: 'raise', amount: parseInt(amount) });
}
function allIn() { socket.emit('player-action', { action: 'allin' }); }

// Check URL params for table invite
window.onload = () => {
    const params = new URLSearchParams(window.location.search);
    const tableId = params.get('table');
    if (tableId) {
        document.getElementById('tableId').value = tableId;
        showJoinForm();
    }
};
