const { v4: uuidv4 } = require('uuid');
const { Deck, evaluateHand, compareHands } = require('./poker');

// Game states
const GAME_STATE = {
  WAITING: 'waiting',
  PREFLOP: 'preflop',
  FLOP: 'flop',
  TURN: 'turn',
  RIVER: 'river',
  SHOWDOWN: 'showdown',
  ENDED: 'ended'
};

const PLAYER_ACTION = {
  FOLD: 'fold',
  CHECK: 'check',
  CALL: 'call',
  RAISE: 'raise',
  ALL_IN: 'allin'
};

class Player {
  constructor(id, name, socketId) {
    this.id = id;
    this.name = name;
    this.socketId = socketId;
    this.chips = 1000; // Starting chips
    this.hand = []; // Hole cards
    this.isActive = true; // Still in current hand
    this.isFolded = false;
    this.currentBet = 0;
    this.totalWon = 0;
    this.totalLost = 0;
    this.handsPlayed = 0;
    this.handsWon = 0;
    this.isDealer = false;
    this.isSmallBlind = false;
    this.isBigBlind = false;
    this.isTurn = false;
  }

  resetForNewHand() {
    this.hand = [];
    this.isActive = true;
    this.isFolded = false;
    this.currentBet = 0;
    this.isDealer = false;
    this.isSmallBlind = false;
    this.isBigBlind = false;
    this.isTurn = false;
  }
}

class Table {
  constructor(id, name, hostId, maxPlayers = 6) {
    this.id = id;
    this.name = name;
    this.hostId = hostId;
    this.maxPlayers = maxPlayers;
    this.players = []; // Array of Player objects
    this.spectators = []; // Players watching but not playing
    
    this.state = GAME_STATE.WAITING;
    this.deck = new Deck();
    this.communityCards = []; // Flop, Turn, River
    this.pot = 0;
    this.currentBet = 0;
    this.smallBlind = 10;
    this.bigBlind = 20;
    
    this.dealerIndex = -1;
    this.currentPlayerIndex = -1;
    this.actionHistory = [];
    this.winners = [];
    
    this.createdAt = Date.now();
    this.lastActivity = Date.now();
  }

  addPlayer(player) {
    if (this.players.length >= this.maxPlayers) {
      return { success: false, error: '牌桌已满' };
    }
    
    if (this.players.find(p => p.id === player.id)) {
      return { success: false, error: '玩家已在牌桌' };
    }
    
    this.players.push(player);
    this.lastActivity = Date.now();
    
    // If game is waiting and we have 2+ players, we could start
    if (this.state === GAME_STATE.WAITING && this.players.length >= 2) {
      // Ready to start, but wait for host
    }
    
    return { success: true };
  }

  removePlayer(playerId) {
    const index = this.players.findIndex(p => p.id === playerId);
    if (index !== -1) {
      this.players.splice(index, 1);
      
      // If game in progress and player was active, handle it
      if (this.state !== GAME_STATE.WAITING && this.state !== GAME_STATE.ENDED) {
        // Fold the player's hand
        const player = this.players[index];
        if (player) {
          player.isFolded = true;
          player.isActive = false;
        }
        this.checkRoundEnd();
      }
      
      this.lastActivity = Date.now();
      return true;
    }
    return false;
  }

  startGame() {
    if (this.players.length < 2) {
      return { success: false, error: '至少需要2名玩家' };
    }
    
    this.state = GAME_STATE.PREFLOP;
    this.deck.reset();
    this.communityCards = [];
    this.pot = 0;
    this.currentBet = 0;
    this.actionHistory = [];
    this.winners = [];
    
    // Reset all players
    this.players.forEach(p => p.resetForNewHand());
    
    // Move dealer button
    this.dealerIndex = (this.dealerIndex + 1) % this.players.length;
    
    // Set blinds
    const sbIndex = (this.dealerIndex + 1) % this.players.length;
    const bbIndex = (this.dealerIndex + 2) % this.players.length;
    
    this.players[this.dealerIndex].isDealer = true;
    this.players[sbIndex].isSmallBlind = true;
    this.players[bbIndex].isBigBlind = true;
    
    // Post blinds
    this.players[sbIndex].chips -= this.smallBlind;
    this.players[sbIndex].currentBet = this.smallBlind;
    
    this.players[bbIndex].chips -= this.bigBlind;
    this.players[bbIndex].currentBet = this.bigBlind;
    
    this.pot = this.smallBlind + this.bigBlind;
    this.currentBet = this.bigBlind;
    
    // Deal hole cards
    this.players.forEach(p => {
      p.hand = [this.deck.deal(), this.deck.deal()];
      p.handsPlayed++;
    });
    
    // First to act is after big blind
    this.currentPlayerIndex = (bbIndex + 1) % this.players.length;
    this.players[this.currentPlayerIndex].isTurn = true;
    
    this.lastActivity = Date.now();
    
    return { success: true };
  }

  performAction(playerId, action, amount = 0) {
    const player = this.players.find(p => p.id === playerId);
    
    if (!player || !player.isTurn) {
      return { success: false, error: '不是你的回合' };
    }
    
    if (player.isFolded || !player.isActive) {
      return { success: false, error: '你已经弃牌' };
    }
    
    const result = this.processAction(player, action, amount);
    
    if (result.success) {
      this.actionHistory.push({
        playerId,
        playerName: player.name,
        action,
        amount,
        timestamp: Date.now()
      });
      
      this.lastActivity = Date.now();
      
      // Move to next player
      this.moveToNextPlayer();
      
      // Check if round should end
      this.checkRoundEnd();
    }
    
    return result;
  }

  processAction(player, action, amount) {
    switch (action) {
      case PLAYER_ACTION.FOLD:
        player.isFolded = true;
        player.isActive = false;
        return { success: true };
        
      case PLAYER_ACTION.CHECK:
        if (player.currentBet < this.currentBet) {
          return { success: false, error: '不能过牌，需要跟注或加注' };
        }
        return { success: true };
        
      case PLAYER_ACTION.CALL:
        const callAmount = this.currentBet - player.currentBet;
        if (player.chips < callAmount) {
          return { success: false, error: '筹码不足' };
        }
        player.chips -= callAmount;
        player.currentBet += callAmount;
        this.pot += callAmount;
        return { success: true };
        
      case PLAYER_ACTION.RAISE:
        const raiseAmount = amount - player.currentBet;
        if (raiseAmount <= 0) {
          return { success: false, error: '加注金额无效' };
        }
        if (player.chips < raiseAmount) {
          return { success: false, error: '筹码不足' };
        }
        player.chips -= raiseAmount;
        player.currentBet += raiseAmount;
        this.currentBet = player.currentBet;
        this.pot += raiseAmount;
        return { success: true };
        
      case PLAYER_ACTION.ALL_IN:
        const allInAmount = player.chips;
        player.currentBet += allInAmount;
        this.pot += allInAmount;
        player.chips = 0;
        if (player.currentBet > this.currentBet) {
          this.currentBet = player.currentBet;
        }
        return { success: true };
        
      default:
        return { success: false, error: '无效操作' };
    }
  }

  moveToNextPlayer() {
    this.players[this.currentPlayerIndex].isTurn = false;
    
    let nextIndex = (this.currentPlayerIndex + 1) % this.players.length;
    let loopCount = 0;
    
    while (loopCount < this.players.length) {
      const nextPlayer = this.players[nextIndex];
      if (nextPlayer.isActive && !nextPlayer.isFolded && nextPlayer.chips > 0) {
        this.currentPlayerIndex = nextIndex;
        nextPlayer.isTurn = true;
        return;
      }
      nextIndex = (nextIndex + 1) % this.players.length;
      loopCount++;
    }
  }

  checkRoundEnd() {
    const activePlayers = this.players.filter(p => p.isActive && !p.isFolded);
    
    // If only one player left, they win
    if (activePlayers.length === 1) {
      this.endHand([activePlayers[0]]);
      return;
    }
    
    // Check if all active players have acted and bets are equal
    const allBetsEqual = activePlayers.every(p => p.currentBet === this.currentBet || p.chips === 0);
    
    if (allBetsEqual) {
      this.advanceStage();
    }
  }

  advanceStage() {
    // Reset current bets for new stage
    this.players.forEach(p => p.currentBet = 0);
    this.currentBet = 0;
    
    switch (this.state) {
      case GAME_STATE.PREFLOP:
        // Deal flop
        this.communityCards.push(this.deck.deal(), this.deck.deal(), this.deck.deal());
        this.state = GAME_STATE.FLOP;
        break;
        
      case GAME_STATE.FLOP:
        // Deal turn
        this.communityCards.push(this.deck.deal());
        this.state = GAME_STATE.TURN;
        break;
        
      case GAME_STATE.TURN:
        // Deal river
        this.communityCards.push(this.deck.deal());
        this.state = GAME_STATE.RIVER;
        break;
        
      case GAME_STATE.RIVER:
        this.state = GAME_STATE.SHOWDOWN;
        this.determineWinners();
        return;
    }
    
    // First to act after flop is small blind (or first active player after dealer)
    let startIndex = (this.dealerIndex + 1) % this.players.length;
    while (!this.players[startIndex].isActive || this.players[startIndex].isFolded) {
      startIndex = (startIndex + 1) % this.players.length;
    }
    
    this.currentPlayerIndex = startIndex;
    this.players[startIndex].isTurn = true;
  }

  determineWinners() {
    const activePlayers = this.players.filter(p => p.isActive && !p.isFolded);
    
    if (activePlayers.length === 1) {
      this.endHand([activePlayers[0]]);
      return;
    }
    
    // Evaluate all hands
    const playerHands = activePlayers.map(player => {
      const allCards = [...player.hand, ...this.communityCards];
      const handEval = evaluateHand(allCards);
      return { player, handEval };
    });
    
    // Sort by hand strength
    playerHands.sort((a, b) => compareHands(b.handEval, a.handEval));
    
    // Find winners (could be tie)
    const bestHand = playerHands[0].handEval;
    const winners = playerHands.filter(ph => compareHands(ph.handEval, bestHand) === 0).map(ph => ph.player);
    
    this.endHand(winners);
  }

  endHand(winners) {
    this.winners = winners;
    this.state = GAME_STATE.ENDED;
    
    // Distribute pot
    const winAmount = Math.floor(this.pot / winners.length);
    winners.forEach(winner => {
      winner.chips += winAmount;
      winner.handsWon++;
      winner.totalWon += winAmount;
    });
    
    // Update losers' stats
    this.players.forEach(p => {
      if (!winners.includes(p)) {
        p.totalLost += p.currentBet;
      }
    });
  }

  getPublicState() {
    return {
      id: this.id,
      name: this.name,
      state: this.state,
      maxPlayers: this.maxPlayers,
      playerCount: this.players.length,
      pot: this.pot,
      currentBet: this.currentBet,
      communityCards: this.communityCards.map(c => ({ suit: c.suit, rank: c.rank })),
      dealerIndex: this.dealerIndex,
      currentPlayerIndex: this.currentPlayerIndex,
      actionHistory: this.actionHistory.slice(-10), // Last 10 actions
      winners: this.winners.map(w => ({ id: w.id, name: w.name }))
    };
  }

  getPlayerState(playerId) {
    const player = this.players.find(p => p.id === playerId);
    if (!player) return null;
    
    return {
      ...this.getPublicState(),
      myHand: player.hand.map(c => ({ suit: c.suit, rank: c.rank })),
      myChips: player.chips,
      myCurrentBet: player.currentBet,
      isMyTurn: player.isTurn,
      isFolded: player.isFolded,
      isDealer: player.isDealer,
      isSmallBlind: player.isSmallBlind,
      isBigBlind: player.isBigBlind,
      players: this.players.map(p => ({
        id: p.id,
        name: p.name,
        chips: p.chips,
        currentBet: p.currentBet,
        isActive: p.isActive,
        isFolded: p.isFolded,
        isDealer: p.isDealer,
        isSmallBlind: p.isSmallBlind,
        isBigBlind: p.isBigBlind,
        isTurn: p.isTurn,
        handCount: p.hand ? p.hand.length : 0 // Only show count, not cards
      }))
    };
  }
}

// Table manager
class TableManager {
  constructor() {
    this.tables = new Map();
  }

  createTable(name, hostId, maxPlayers = 6) {
    const id = uuidv4().slice(0, 8); // Short ID for easy sharing
    const table = new Table(id, name, hostId, maxPlayers);
    this.tables.set(id, table);
    return table;
  }

  getTable(id) {
    return this.tables.get(id);
  }

  removeTable(id) {
    return this.tables.delete(id);
  }

  getAllTables() {
    return Array.from(this.tables.values()).map(t => t.getPublicState());
  }

  cleanupInactiveTables(maxAge = 24 * 60 * 60 * 1000) { // 24 hours
    const now = Date.now();
    for (const [id, table] of this.tables) {
      if (now - table.lastActivity > maxAge) {
        this.tables.delete(id);
      }
    }
  }
}

module.exports = {
  Player,
  Table,
  TableManager,
  GAME_STATE,
  PLAYER_ACTION
};
