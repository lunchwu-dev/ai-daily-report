// Texas Hold'em Poker Game Logic

const SUITS = ['♠', '♥', '♦', '♣'];
const RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];

class Card {
  constructor(suit, rank) {
    this.suit = suit;
    this.rank = rank;
    this.value = RANKS.indexOf(rank);
  }

  toString() {
    return `${this.suit}${this.rank}`;
  }

  getColor() {
    return this.suit === '♥' || this.suit === '♦' ? 'red' : 'black';
  }
}

class Deck {
  constructor() {
    this.cards = [];
    this.reset();
  }

  reset() {
    this.cards = [];
    for (const suit of SUITS) {
      for (const rank of RANKS) {
        this.cards.push(new Card(suit, rank));
      }
    }
    this.shuffle();
  }

  shuffle() {
    for (let i = this.cards.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
    }
  }

  deal() {
    return this.cards.pop();
  }
}

// Hand ranking evaluation
const HAND_RANKINGS = {
  ROYAL_FLUSH: 10,
  STRAIGHT_FLUSH: 9,
  FOUR_OF_A_KIND: 8,
  FULL_HOUSE: 7,
  FLUSH: 6,
  STRAIGHT: 5,
  THREE_OF_A_KIND: 4,
  TWO_PAIR: 3,
  ONE_PAIR: 2,
  HIGH_CARD: 1
};

function evaluateHand(cards) {
  // Sort by value descending
  const sorted = [...cards].sort((a, b) => b.value - a.value);
  
  const isFlush = checkFlush(sorted);
  const isStraight = checkStraight(sorted);
  const rankCounts = getRankCounts(sorted);
  
  // Check Royal Flush
  if (isFlush && isStraight && sorted[0].value === 12) {
    return { rank: HAND_RANKINGS.ROYAL_FLUSH, name: '皇家同花顺', cards: sorted.slice(0, 5) };
  }
  
  // Check Straight Flush
  if (isFlush && isStraight) {
    return { rank: HAND_RANKINGS.STRAIGHT_FLUSH, name: '同花顺', cards: sorted.slice(0, 5) };
  }
  
  // Check Four of a Kind
  const fourOfAKind = findNOfAKind(rankCounts, 4);
  if (fourOfAKind) {
    const kicker = sorted.find(c => c.value !== fourOfAKind);
    return { rank: HAND_RANKINGS.FOUR_OF_A_KIND, name: '四条', cards: [...getCardsByValue(sorted, fourOfAKind), kicker] };
  }
  
  // Check Full House
  const threeOfAKind = findNOfAKind(rankCounts, 3);
  const pair = findPairExcluding(rankCounts, threeOfAKind);
  if (threeOfAKind && pair) {
    return { rank: HAND_RANKINGS.FULL_HOUSE, name: '葫芦', cards: [...getCardsByValue(sorted, threeOfAKind), ...getCardsByValue(sorted, pair)] };
  }
  
  // Check Flush
  if (isFlush) {
    return { rank: HAND_RANKINGS.FLUSH, name: '同花', cards: getFlushCards(sorted) };
  }
  
  // Check Straight
  if (isStraight) {
    return { rank: HAND_RANKINGS.STRAIGHT, name: '顺子', cards: getStraightCards(sorted) };
  }
  
  // Check Three of a Kind
  if (threeOfAKind) {
    const kickers = sorted.filter(c => c.value !== threeOfAKind).slice(0, 2);
    return { rank: HAND_RANKINGS.THREE_OF_A_KIND, name: '三条', cards: [...getCardsByValue(sorted, threeOfAKind), ...kickers] };
  }
  
  // Check Two Pair
  const pairs = findAllPairs(rankCounts);
  if (pairs.length >= 2) {
    const kicker = sorted.find(c => !pairs.includes(c.value));
    return { rank: HAND_RANKINGS.TWO_PAIR, name: '两对', cards: [...getCardsByValue(sorted, pairs[0]), ...getCardsByValue(sorted, pairs[1]), kicker] };
  }
  
  // Check One Pair
  if (pairs.length === 1) {
    const kickers = sorted.filter(c => c.value !== pairs[0]).slice(0, 3);
    return { rank: HAND_RANKINGS.ONE_PAIR, name: '一对', cards: [...getCardsByValue(sorted, pairs[0]), ...kickers] };
  }
  
  // High Card
  return { rank: HAND_RANKINGS.HIGH_CARD, name: '高牌', cards: sorted.slice(0, 5) };
}

function checkFlush(cards) {
  const suitCounts = {};
  for (const card of cards) {
    suitCounts[card.suit] = (suitCounts[card.suit] || 0) + 1;
  }
  return Object.values(suitCounts).some(count => count >= 5);
}

function checkStraight(cards) {
  const uniqueValues = [...new Set(cards.map(c => c.value))];
  if (uniqueValues.length < 5) return false;
  
  for (let i = 0; i <= uniqueValues.length - 5; i++) {
    if (uniqueValues[i] - uniqueValues[i + 4] === 4) return true;
  }
  
  // Check A-2-3-4-5 straight
  if (uniqueValues.includes(12) && uniqueValues.includes(0) && 
      uniqueValues.includes(1) && uniqueValues.includes(2) && uniqueValues.includes(3)) {
    return true;
  }
  
  return false;
}

function getRankCounts(cards) {
  const counts = {};
  for (const card of cards) {
    counts[card.value] = (counts[card.value] || 0) + 1;
  }
  return counts;
}

function findNOfAKind(rankCounts, n) {
  for (const [value, count] of Object.entries(rankCounts)) {
    if (count === n) return parseInt(value);
  }
  return null;
}

function findPairExcluding(rankCounts, excludeValue) {
  for (const [value, count] of Object.entries(rankCounts)) {
    if (count >= 2 && parseInt(value) !== excludeValue) return parseInt(value);
  }
  return null;
}

function findAllPairs(rankCounts) {
  const pairs = [];
  for (const [value, count] of Object.entries(rankCounts)) {
    if (count >= 2) pairs.push(parseInt(value));
  }
  return pairs.sort((a, b) => b - a);
}

function getCardsByValue(cards, value) {
  return cards.filter(c => c.value === value);
}

function getFlushCards(cards) {
  const suitCounts = {};
  for (const card of cards) {
    suitCounts[card.suit] = (suitCounts[card.suit] || []);
    suitCounts[card.suit].push(card);
  }
  
  for (const suitCards of Object.values(suitCounts)) {
    if (suitCards.length >= 5) return suitCards.slice(0, 5);
  }
  return cards.slice(0, 5);
}

function getStraightCards(cards) {
  const uniqueValues = [...new Set(cards.map(c => c.value))];
  
  for (let i = 0; i <= uniqueValues.length - 5; i++) {
    if (uniqueValues[i] - uniqueValues[i + 4] === 4) {
      const straightCards = [];
      for (let v = uniqueValues[i]; v >= uniqueValues[i + 4]; v--) {
        straightCards.push(cards.find(c => c.value === v));
      }
      return straightCards;
    }
  }
  
  // A-2-3-4-5
  if (uniqueValues.includes(12) && uniqueValues.includes(0)) {
    return [cards.find(c => c.value === 12), cards.find(c => c.value === 3),
            cards.find(c => c.value === 2), cards.find(c => c.value === 1),
            cards.find(c => c.value === 0)];
  }
  
  return cards.slice(0, 5);
}

function compareHands(hand1, hand2) {
  if (hand1.rank !== hand2.rank) {
    return hand1.rank - hand2.rank;
  }
  
  // Same rank, compare kickers
  for (let i = 0; i < Math.min(hand1.cards.length, hand2.cards.length); i++) {
    if (hand1.cards[i].value !== hand2.cards[i].value) {
      return hand1.cards[i].value - hand2.cards[i].value;
    }
  }
  
  return 0; // Tie
}

module.exports = {
  Card,
  Deck,
  evaluateHand,
  compareHands,
  HAND_RANKINGS
};
