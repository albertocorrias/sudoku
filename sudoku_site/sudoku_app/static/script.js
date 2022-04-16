import Game from "./Game.js"


const puzzle_hints = JSON.parse(document.getElementById('puzzle_hints').textContent);
const puzzle_solution = JSON.parse(document.getElementById('puzzle_solution').textContent);
console.log(puzzle_solution)
const new_game = new Game(puzzle_hints,puzzle_solution);
