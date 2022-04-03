import Grid from "./Grid.js"

export default class Game {

    constructor() {
        const gameBoard = document.getElementById("game-board")
        const grid = new Grid(gameBoard)
        grid.setUpEventListeners();
        var all_cells = grid.cells;
        const starting_pont = [1,2,3,4,5,6,7,8,9]
        //solution of first row
        const first_row = starting_pont.sort((a, b) => 0.5 - Math.random());
        //Put values of first row in grid
        const grid_indices_of_first_row = grid.getIndicesOnSameRow(0)
        for (let i=0; i < grid_indices_of_first_row.length; i++){
            all_cells[grid_indices_of_first_row[i]].value = first_row[i]
        }

        var second_row = [Globals.GRID_SIZE]
        const row_index = 1;//second row for now...loop later
        for (let pos_in_row = 0; pos_in_row < Globals.GRID_SIZE; pos_in_row++){
            //position in this row
            const current_position = Globals.GRID_SIZE*(row_index) + pos_in_row
            
            const indices_on_same_row = grid.getIndicesOnSameRow(current_position)
            const indices_on_same_column = grid.getIndicesOnSameColumn(current_position)
            const indices_on_same_quadrant = grid.getIndicesOnSameQuadrant(current_position)
            var forbidden_values = []
            for (let i = 0; i < Globals.GRID_SIZE; i++) {
                const num_on_same_row = all_cells[indices_on_same_row[i]].value
                if (num_on_same_row != null){
                    forbidden_values.push(num_on_same_row)    
                }
                const num_on_same_col = all_cells[indices_on_same_column[i]].value
                if (num_on_same_col != null){
                    forbidden_values.push(num_on_same_col)    
                }
                const num_on_same_quad = all_cells[indices_on_same_quadrant[i]].value
                if (num_on_same_quad != null){
                    forbidden_values.push(num_on_same_quad)    
                }
            }

            var possible_values = [];
            //add possible values
            for (let i =0; i < starting_pont.length; i++) {
                const to_be_added = starting_pont[i]
                if (forbidden_values.includes(to_be_added) == false){
                    possible_values.push(to_be_added)
                }
            }
            //shuffle possible values
            //possible_values = possible_values.sort();
            //all_cells[current_position].value = possible_values[0]

            console.log(forbidden_values)
            console.log(possible_values)
        }
    }


}