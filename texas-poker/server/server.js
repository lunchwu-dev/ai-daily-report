const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const { Player, Table, TableManager, GAME_STATE, PLAYER_ACTION } = require('./table');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

const tableManager = new TableManager();

// Serve static files
app.use(express.static(path.join(__dirname, '../client')));
app.use(cors());

// API Routes
app.get('/api/tables', (req, res) => {
  res.json(tableManager.getAllTables());
});

app.get('/api/table/:id', (req, res) => {
  const table = tableManager.getTable(req.params.id);
  if (!table) {
    return res.status(404).json({ error: '牌桌不存在' });
  }
  res.json(table.getPublicState());
});

// Socket.IO handling
io.on('connection', (socket) => {
  console.log('Player connected:', socket.id);
  
  let currentPlayer = null;
  let currentTable = null;

  // Create new table
  socket.on('create-table', ({ tableName, playerName, maxPlayers = 6 }) => {
    const playerId = uuidv4();
    currentPlayer = new Player(playerId, playerName, socket.id);
    
    const table = tableManager.createTable(tableName, playerId, maxPlayers);
    const result = table.addPlayer(currentPlayer);
    
    if (result.success) {
      currentTable = table;
      socket.join(table.id);
      
      socket.emit('table-created', {
        tableId: table.id,
        playerId: playerId,
        table: table.getPublicState()
      });
      
      // Notify all players in table
      io.to(table.id).emit('player-joined', {
        player: { id: playerId, name: playerName },
        table: table.getPublicState()
      });
    } else {
      socket.emit('error', result.error);
    }
  });

  // Join existing table
  socket.on('join-table', ({ tableId, playerName }) => {
    const table = tableManager.getTable(tableId);
    
    if (!table) {
      return socket.emit('error', '牌桌不存在');
    }
    
    if (table.state !== GAME_STATE.WAITING) {
      return socket.emit('error', '游戏已开始，无法加入');
    }
    
    const playerId = uuidv4();
    currentPlayer = new Player(playerId, playerName, socket.id);
    
    const result = table.addPlayer(currentPlayer);
    
    if (result.success) {
      currentTable = table;
      socket.join(table.id);
      
      socket.emit('joined-table', {
        tableId: table.id,
        playerId: playerId,
        table: table.getPublicState()
      });
      
      // Notify all players
      io.to(table.id).emit('player-joined', {
        player: { id: playerId, name: playerName },
        table: table.getPublicState()
      });
    } else {
      socket.emit('error', result.error);
    }
  });

  // Start game
  socket.on('start-game', () => {
    if (!currentTable || !currentPlayer) return;
    
    if (currentTable.hostId !== currentPlayer.id) {
      return socket.emit('error', '只有房主可以开始游戏');
    }
    
    const result = currentTable.startGame();
    
    if (result.success) {
      // Send game state to all players
      currentTable.players.forEach(player => {
        const playerState = currentTable.getPlayerState(player.id);
        io.to(player.socketId).emit('game-started', playerState);
      });
    } else {
      socket.emit('error', result.error);
    }
  });

  // Player action
  socket.on('player-action', ({ action, amount }) => {
    if (!currentTable || !currentPlayer) return;
    
    const result = currentTable.performAction(currentPlayer.id, action, amount);
    
    if (result.success) {
      // Broadcast updated state to all players
      currentTable.players.forEach(player => {
        const playerState = currentTable.getPlayerState(player.id);
        io.to(player.socketId).emit('game-update', playerState);
      });
      
      // Check if hand ended
      if (currentTable.state === GAME_STATE.ENDED) {
        io.to(currentTable.id).emit('hand-ended', {
          winners: currentTable.winners.map(w => ({ id: w.id, name: w.name })),
          pot: currentTable.pot
        });
      }
    } else {
      socket.emit('error', result.error);
    }
  });

  // Get table state
  socket.on('get-table-state', () => {
    if (!currentTable || !currentPlayer) return;
    
    const playerState = currentTable.getPlayerState(currentPlayer.id);
    socket.emit('table-state', playerState);
  });

  // Leave table
  socket.on('leave-table', () => {
    if (currentTable && currentPlayer) {
      currentTable.removePlayer(currentPlayer.id);
      socket.leave(currentTable.id);
      
      io.to(currentTable.id).emit('player-left', {
        playerId: currentPlayer.id,
        playerName: currentPlayer.name,
        table: currentTable.getPublicState()
      });
      
      currentTable = null;
      currentPlayer = null;
    }
  });

  // Disconnect
  socket.on('disconnect', () => {
    console.log('Player disconnected:', socket.id);
    
    if (currentTable && currentPlayer) {
      currentTable.removePlayer(currentPlayer.id);
      
      io.to(currentTable.id).emit('player-disconnected', {
        playerId: currentPlayer.id,
        playerName: currentPlayer.name,
        table: currentTable.getPublicState()
      });
    }
  });
});

// Cleanup inactive tables every hour
setInterval(() => {
  tableManager.cleanupInactiveTables();
}, 60 * 60 * 1000);

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Texas Poker Server running on port ${PORT}`);
});
