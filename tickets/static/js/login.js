var frm = $('login-form');
frm.submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            if (data.result === false) {
                $("#answer").html('<p1>' + data.message + '</p1><br>').css("color", "red").animate("slow");
            }
            console.log(data);
        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        }
    });
});