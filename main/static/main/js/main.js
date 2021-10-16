$('.waitlist').on('click', function () {
    var data = {
        email: $('#email').val(),
        lastname: $('#lastname').val(),
        firstname: $('#firstname').val()
    }
    console.log(data.email)

    $.ajax({
        type: "POST",
        url: window.location,
        data: {
            'csrfmiddlewaretoken': T,
            'data': JSON.stringify(data)
        },
        success: function () {
            console.log('done')
        }
    });
})