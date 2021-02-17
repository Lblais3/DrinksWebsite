$(document).ready(function() {

    setupAutocomplete();

    // Adds a qty/unit/ingredient row to table
    $(".addrow").on("click", function () {
        var newRow = $("<tr>");
        var cols = "";

        cols += '<td><input type="text" class="form-control" name="qty"/></td>';
        cols += '<td><input type="text" class="form-control" name="unit"/></td>';
        cols += '<td><input type="text" class="form-control autocomplete" name="ingredient"/></td>';

        if ($(this).parents("#muddle_ingredients").length > 0) {
        cols += '<input type="hidden" name="ing_category" value="muddle"/>';
        }

        if ($(this).parents("#primary_ingredients").length > 0) {
        cols += '<input type="hidden" name="ing_category" value="primary"/>';
        }

        if ($(this).parents("#garnish_ingredients").length > 0) {
        cols += '<input type="hidden" name="ing_category" value="garnish"/>';
        }


        cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        newRow.append(cols);
        $(this).closest("table.order-list").append(newRow)
        setupAutocomplete();
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

    // Autocomplete js script ripped from: https://stackoverflow.com/questions/34704997/jquery-autocomplete-in-flask
    // Changed selector to be by class autocomplete instead of id
    function setupAutocomplete() {
        $(".autocomplete").autocomplete({
            source:function(request, response) {
                var nameID = this.element.attr('name');
                $.getJSON("/autocomplete",
                {q: request.term, n: nameID},
                function(data) {
                    response(data.matching_results); // matching_results from jsonify
                });
            },
            minLength: 2,
            select: function(event, ui) {
                console.log(ui.item.value); // not in your question, but might help later
            }
        });
    }

    /* Refreshes List of Ingredients to select for Muddling
    $("#muddleRefresh").on("click", function() {
        var ingredients = $(".ingredients").val();

        var rows = ;

        for (var i = 0; i < ingredients.length; i++) {
            cols += "<>"
        }
    })
    */
});