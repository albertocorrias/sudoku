import Grid from "./Grid.js"
import Cell from "./Cell.js"

const gameBoard = document.getElementById("game-board")

const grid = new Grid(gameBoard)
grid.setUpEventListeners();
