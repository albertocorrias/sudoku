import Grid from "./Grid.js"

export default class Game {

    constructor(hints,solution) {
        const gameBoard = document.getElementById("game-board")
        const grid = new Grid(gameBoard)

        const cells_collection = document.getElementsByClassName("cell");
        var all_cells = grid.cells;

        //hide the resume play
        document.getElementById("resume_play_button").style.setProperty("--resume-play-visibility","none")
        //hide the overlay that appears fro timed session when user submits
        document.getElementById("id_overlay_timed_results").style.setProperty("--overlay-timed-results-visibility", "none")
        
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
            cells_collection[i].style.setProperty("--text-size", "100%")//set text size as default
            
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
                    //handle digits 
                    if (isFinite(evt.key) == true && evt.key != "0") {//note we exclue 0, not part of the game
                        grid.insertDigitIntoCell(i,evt.key)
                    }

                    if (evt.key == "Backspace" || evt.key == "Delete") {
                        grid.clearCellValue(i)
                        cells_collection[i].focus()
                    }

                    if (evt.key == "p") {
                        all_cells[i].cellElement.style.setProperty("--number-color",Globals.NUMBER_COLOR_OF_PROVISIONAL_NUMBERS)
                        all_cells[i].cellElement.style.setProperty("--text-size", "50%")
                        all_cells[i].isProvisional = true
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
        
        //setup event listener for numpad keys
        for (let i = 0; i < Globals.GRID_SIZE; i++) {
            const id_name = "numpad-item-" + String(i+1)
            document.getElementById(id_name).addEventListener("click", function(evt) {
                for (let k = 0; k < all_cells.length; k++) {
                    if (all_cells[k].isClicked == true) {
                        grid.insertDigitIntoCell(k,i+1)

                        grid.clearAllHighlighting()
                        grid.highlightRelatedCells(k)
                        grid.highlightCell(k)
                        grid.highlightEqualValues(k)
                        cells_collection[k].focus()
                    }
                }

            }, true)
        }

        //setup event listener for "P" button on the keypad next to the game board
        document.getElementById("provisional-button").addEventListener("click", function(evt) {
            for (let i = 0; i < all_cells.length; i++) {
                if (all_cells[i].isClicked == true) {
                    all_cells[i].cellElement.style.setProperty("--number-color",Globals.NUMBER_COLOR_OF_PROVISIONAL_NUMBERS)
                    all_cells[i].cellElement.style.setProperty("--text-size", "50%")
                    all_cells[i].isProvisional = true
                    all_cells[i].cellElement.focus()
                }
            }
        }, true)

        //setup event listener for "Del" button on the keypad next to the game board
        document.getElementById("delete-button").addEventListener("click", function(evt) {
            for (let i = 0; i < all_cells.length; i++) {
                if (all_cells[i].isClicked == true) {
                    grid.clearCellValue(i)
                    cells_collection[i].focus()
                }
            }
        }, true)

        //setup event listener for submit button
        document.getElementById("check_answers_button").addEventListener("click", function(evt) {
            grid.clearAllHighlighting()
            var cell_counter = 0
            var drop_down_type = document.getElementById("id_game_type")
            var selected_value = drop_down_type.options[drop_down_type.selectedIndex].value
            var timed = false
            if (selected_value == "Timed") { timed = true}

            var all_correct = true
            for (let i=0; i < solution.length; i++){
                for (let j=0; j < solution[i].length; j++){
                    if (all_cells[cell_counter].isHint == false) {//we do not bother hints...
                        if ( all_cells[cell_counter].value == solution[i][j] ){
                            if (timed == false){
                                all_cells[cell_counter].cellElement.style.setProperty("--cell-background-colour",Globals.CORRECT_ANSWER_BG_COLOUR)
                            }
                            
                        } else {
                            if (timed == false) {
                                all_cells[cell_counter].cellElement.style.setProperty("--cell-background-colour",Globals.WRONG_ANSWER_BG_COLOUR)
                            }
                            all_correct = false
                        }
                    }
                    cell_counter = cell_counter + 1
                }
            }
            //If it is not a timed sesssion, then just either congratulate or allow play to resume after highlighting
            if (timed == false) {
                if (all_correct == true) {
                    alert("Well done! Your solution is correct!")
                }
                document.getElementById("resume_play_button").style.setProperty("--resume-play-visibility","inline")
            } else {//this is a timed session
                document.getElementById("id_overlay_timed_results").style.setProperty("--overlay-timed-results-visibility", "block")
                if (all_correct == true) {
                    document.getElementById("id_overlay_paragraph").innerHTML = "Well done! Your solution is correct"
                    ///\TODO send to server for storing
                    console.log("********************* HELLO")
                    
                } else {
                    document.getElementById("id_overlay_paragraph").innerHTML = "Your answer is incorrect or incomplete"
                    ///\TODO Count number of wrong times
                }
            }
        }, true)

        //setup event listener for resume play button (for leisure plays)
        document.getElementById("resume_play_button").addEventListener("click", function(evt) {
            grid.clearAllHighlighting()
            document.getElementById("resume_play_button").style.setProperty("--resume-play-visibility","none")
        }, true)

        //setup event listener for closing the overlay
        document.getElementById("id_close_timed_results_overlay_button").addEventListener("click", function(evt){
            //just hide the overlay
            document.getElementById("id_overlay_timed_results").style.setProperty("--overlay-timed-results-visibility", "none")
        }, true)

    }//constructor
}//Game class


