var id_res;

function display_concerts(data) {
    for (var i = 0; i < data.length; i++) {
        var id_number = i + 1;
        var row = "<td class='reservations-row'>" + id_number + "</td>";
        for (var x in data[i]) {
            if(x === "id"){
                var id = data[i][x]
                var form_id = "form-" + id;
            }
            else {
                row += '<td id="' + x + "-" + i + '">' + data[i][x] + '</td>';
            }
        }

        var tr_id = "ticket-table-row-" + i;
        row += "<td><button class='btn btn-danger cancel-reservation-btn' type='submit' onclick=\"cancel(" + id + ")\">Cancel reservation</button></td>";
        $('#reservations-table tbody').append('<tr class="table-element" id=' + tr_id + '>' + row + '</tr>').css({
            "margin": "auto",
            "width": "70%", "color": "black"
        })
    }
}


function get_reservations() {
    $.ajax({
        type: "GET",
        url: "profile_table",
        success: function (data) {
            display_concerts(data);
        },
        error: function (data) {
            console.log('error');
            console.log(data)
        }
    });
}

function cancel(id) {

    $.ajax({
        type: "GET",
        url: "cancel_reservations/"+id,
        success: function (data) {
            console.log("succes");
            $('#reservations-table tbody').html("");
            get_reservations();
        },
        error: function (data) {
            console.log('error');
            console.log(data)
        }
    });

}


$(document).ready(function (e) {
    get_reservations();
    $("#search").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#reservations-table tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});