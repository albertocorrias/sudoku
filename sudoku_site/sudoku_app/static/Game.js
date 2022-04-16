import Grid from "./Grid.js"

export default class Game {

    constructor(hints,solution) {
        const gameBoard = document.getElementById("game-board")
        const grid = new Grid(gameBoard)
        
        var all_cells = grid.cells;

        //Put hints
        var cell_counter = 0
        for (let i=0; i < hints.length; i++){
            for (let j=0; j < hints[i].length; j++){
                if (hints[i][j] > 0) {
                    all_cells[cell_counter].value = hints[i][j]
                    all_cells[cell_counter].isHint = true
                }
                cell_counter = cell_counter + 1
            }
        }

        grid.setUpEventListeners();
        
    }


}