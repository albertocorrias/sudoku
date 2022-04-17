import Grid from "./Grid.js"

export default class Game {

    constructor(hints,solution) {
        const gameBoard = document.getElementById("game-board")
        const grid = new Grid(gameBoard)

        const cells_collection = document.getElementsByClassName("cell");
        var all_cells = grid.cells;

        //Put hints
        var cell_counter = 0
        for (let i=0; i < hints.length; i++){
            for (let j=0; j < hints[i].length; j++){
                if (hints[i][j] > 0) {
                    all_cells[cell_counter].value = hints[i][j]
                    all_cells[cell_counter].isHint = true
                    all_cells[cell_counter].cellElement.style.setProperty("--number-color",Globals.NUMBER_COLOR_OF_HINTS)
                }
                cell_counter = cell_counter + 1
            }
        }
        
        //setup event listeners for all cells
        for (let i = 0; i < cells_collection.length; i++) {
            cells_collection[i].setAttribute("tabindex", 0)//critical line to allow focus and accepting key events
            //Handle clicks
            cells_collection[i].addEventListener("click", function(evt) {
                grid.clearAllHighlighting()
                grid.highlightRelatedCells(i)
                grid.highlightCell(i)
                grid.highlightEqualValues(i)
                cells_collection[i].focus() //unnecessary?
            }, true)
            //handle key inputs
            cells_collection[i].addEventListener("keydown", function(evt) {
                //accept number and delete key inputs only from non-hints cells. Hints should not change
                if (all_cells[i].isHint == false) {
                    //handle digits and delete activities
                    if (isFinite(evt.key) == true) {
                        all_cells[i].value = evt.key;//record new values
                    }
                    if (evt.key == "Backspace" || evt.key == "Delete") {
                        all_cells[i].value = undefined //back to undefined value
                    }
                    grid.clearAllHighlighting()
                    grid.highlightRelatedCells(i)
                    grid.highlightCell(i)
                    grid.highlightEqualValues(i)
                    cells_collection[i].focus() //unnecessary?
                }
                //handle arrow keys
                var new_index = -1;
                if (evt.key === "ArrowUp"){ new_index = grid.getIndexOfCellAbove(i)}
                if (evt.key === "ArrowRight"){ new_index = grid.getIndexOfCellAtRight(i)}
                if (evt.key === "ArrowLeft"){ new_index = grid.getIndexOfCellAtLeft(i)}
                if (evt.key === "ArrowDown"){ new_index = grid.getIndexOfCellBelow(i)}
                if (new_index > -1) {
                    grid.clearAllHighlighting()
                    grid.highlightRelatedCells(new_index)
                    grid.highlightCell(new_index)
                    grid.highlightEqualValues(new_index)
                    cells_collection[i].blur()//focus out of previous cell
                    cells_collection[new_index].focus()//allow for successive presses...
                }         
            }) 
        }        
    }//constructor
}//Game class