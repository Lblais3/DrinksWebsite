$(document).ready(function() {

    // Adds a qty/unit/ingredient row to table
    $("#addrow").on("click", function () {
        var newRow = $("<tr>");
        var cols = "";

        cols += '<td><input type="text" class="form-control" name="qty"/></td>';
        cols += '<td><input type="text" class="form-control" name="unit"/></td>';
        cols += '<td><input type="text" class="form-control" name="ingredient"/></td>';

        cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        newRow.append(cols);
        $("table.order-list").append(newRow);
    });

    $("table.order-list").on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();
    });

    // Dynamically sets sibling input value to whats being typed.
    // Will break if more than 2 inputs in generation
    $(".other_input").keyup(function(){
        var val = $(this).val();
        $(this).siblings($("input")).val(val);
    });

    // Refreshes List of Ingredients to select for Muddling
    $("#muddleRefresh").on("click", function() {
        var ingredients = $(".ingredients").val();

        var rows = ;

        for (var i = 0; i < ingredients.length; i++) {
            cols += "<>"
        }


    })



});