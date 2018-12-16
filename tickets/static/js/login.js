$("#login").click(function () {
    var form = $('.login-form');
    $.ajax({
        type: "POST",
        url: "buy",
        dataType: 'json',
        data: form.serialize(),
        success: function (data) {
            if(data.status === 200){
                $(this).unbind('submit').submit()
            }
            $("#answer").html('<p1>' + data.message + '</p1><br>').css("color", "red").animate("slow");
            console.log(data)
        },
        error: function (data) {
            console.log('error');
            console.log(data)
        }
    });
});