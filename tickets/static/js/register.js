$('.message a').click(function () {
    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});


var frm = $('#register-form');
frm.submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        data: frm.serialize(),
        success: function (data) {
            if (data.result === true) {
                $("#answer").html('<p1>' + data.message + '</p1><br>').css("color", "#5faf30").animate("slow");
                $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
            }
            else {
                if (Object.keys(data.message)[0] === "username") {
                    $("#answer").html('<p1>' + data.message[Object.keys(data.message)[0]] + '</p1><br>').css("color", "red").animate("slow");
                }
            }
            console.log(data);
        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        }
    });
});
