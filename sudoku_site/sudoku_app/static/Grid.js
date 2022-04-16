import Cell from "./Cell.js"


export default class Grid {
    #cells
    #onerow
    #onecolumn
    #onequadrant

    constructor(gridElement) {
        gridElement.style.setProperty("--grid-size", Globals.GRID_SIZE)
        gridElement.style.setProperty("--cell-size", `${Globals.CELL_SIZE}vmin`)
        gridElement.style.setProperty("--board-border", `${Globals.BOARD_BORDER_WIDTH}vmin`)
        
        /*Create the cells*/
        this.#cells = createCellElements(gridElement).map((cellElement, index) => {
            return new Cell(cellElement, 
                index % Globals.GRID_SIZE, 
                Math.floor(index / Globals.GRID_SIZE))
        })
    }

    get cells() {
        return this.#cells;
    }

    getIndicesOnSameRow(idx) {
        let ret = [Globals.GRID_SIZE]
        let y_ref = this.#cells[idx].y
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].y == y_ref) {
                ret[counter] = i
                counter = counter +1
            }
        }
        return ret;
    }

    getIndicesOnSameColumn(idx) {
        let ret = [Globals.GRID_SIZE]
        let x_ref = this.#cells[idx].x
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].x == x_ref) {
                ret[counter] = i
                counter = counter +1
            }
        }
        return ret;
    }

    getIndicesOnSameQuadrant(idx) {
        let ret = [Globals.GRID_SIZE]
        let quad_ref = this.#cells[idx].quadrant
        let counter = 0
        for (let i = 0; i < this.#cells.length; i++) {
            if (this.#cells[i].quadrant == quad_ref) {
                ret[counter] = i
                counter = counter +1
            }
        }
        return ret;
    }

    setUpEventListeners() {
        const cells_collection = document.getElementsByClassName("cell");
        let all_cells = this.#cells
        for (let i = 0; i < cells_collection.length; i++) {
            cells_collection[i].setAttribute("tabindex", 0)//critical line to allow focus and accepting key events
            
            let on_same_row = this.getIndicesOnSameRow(i)
            let on_same_column = this.getIndicesOnSameColumn(i)
            let on_same_quadrant = this.getIndicesOnSameQuadrant(i)
            cells_collection[i].addEventListener("click", function() {
                //clear any previous highlighting
                for (let j = 0; j < cells_collection.length; j++) {
                    let elem_to_clear = all_cells[j].cellElement
                    elem_to_clear.style.setProperty("--cell-background-colour", Globals.NORMAL_CELL_COLOR)
                }
                //highlight same row, same column and same quadrant
                for (let k = 0; k < on_same_row.length; k++){
                    let elem_same_row = all_cells[on_same_row[k]].cellElement
                    let elem_same_col = all_cells[on_same_column[k]].cellElement
                    let elem_same_quad = all_cells[on_same_quadrant[k]].cellElement
                    
                    elem_same_row.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_RELATED_CELL_COLOR)
                    elem_same_col.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_RELATED_CELL_COLOR)
                    elem_same_quad.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_RELATED_CELL_COLOR)
                }
                //highlight equal values elsewhere
                for (let j = 0; j < cells_collection.length; j++) {
                    if (all_cells[j].value==all_cells[i].value && typeof all_cells[j].value != 'undefined') {
                        let elem_to_highlight = all_cells[j].cellElement
                        elem_to_highlight.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR_SAME_NUMBER)
                    }
                }
                //highlight the clicked cell itself
                let elem_clicked = all_cells[i].cellElement
                elem_clicked.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR)
            })

            //accept key inputs only from non-hints cells
            if (all_cells[i].isHint == false) {
                cells_collection[i].addEventListener('keydown', function(e) {
                    console.log(i) //DEBUG LINE.    
                    //restrict to digit only
                    if ((e.code.includes("Numpad") == true || e.code.includes("Digit") == true) == false) {
                        e.preventDefault();
                        return false;//do no more
                    }
                    for (let j = 0; j < cells_collection.length; j++) {
                        //clear previous highlighting
                        if (all_cells[j].cellElement.style.getPropertyValue("--cell-background-colour") == Globals.HIGHLIGHTED_CELL_COLOR_SAME_NUMBER) {
                            //restore same-quadrant-same-row-same-column highlighting where necessary
                            if (on_same_row.includes(j) || on_same_column.includes(j) || on_same_quadrant.includes(j)){
                                all_cells[j].cellElement.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_RELATED_CELL_COLOR)
                            } else {
                                //restore normal background otherwise
                                all_cells[j].cellElement.style.setProperty("--cell-background-colour", Globals.NORMAL_CELL_COLOR)
                            }
                        }
                        //impose new hoghlighting
                        if (all_cells[j].value==e.key && typeof all_cells[j].value != 'undefined') {
                            let elem_to_highlight = all_cells[j].cellElement
                            elem_to_highlight.style.setProperty("--cell-background-colour", Globals.HIGHLIGHTED_CELL_COLOR_SAME_NUMBER)
                        }
                    }
                    all_cells[i].value = e.key;//record new value
                });
            }
        }
    }
} //end of Grid class

function createCellElements(gridElement) {
    const cells = []
    for (let i = 0; i < Globals.GRID_SIZE * Globals.GRID_SIZE; i++){
        var cell = document.createElement("div")
        cell.setAttribute('id', `divcell-${i}`);
        cell.classList.add("cell")
        cells.push(cell)
        gridElement.append(cell)
    }
    return cells
}


