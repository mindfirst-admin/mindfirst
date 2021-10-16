// main page
$('.hover_show').click(function() {
    $('#hover-show-div').toggleClass('active')

    src = $(this).attr("src")
    image = $('#hover-show-div').find('img')
    image.prop('src', src)
})

function close_hover_show() {
$('#hover-show-div').toggleClass("active")
}

// edit pages
function ask_delete() {
    $('#confirm_deletion').toggleClass('active')
}

function close_delete() {
    $('#confirm_deletion').toggleClass('active')
}

function actual_delete() {
    $("#checkbox_form").submit()
}

function upload(e) {
    $("#upload_files").submit()
}

function save_images() {
    $("#add_to_values").submit()
}

function check_delete(es) {
    if ($( es ).is(':checked')) {
        $("#delete_btn").attr("disabled", false);
    } else {
        var all_checkboxes = $('body').find('input[type=checkbox]:checked')
        if (all_checkboxes.length != 0) {
            $("#delete").attr("disabled", false);
        } else {
            $("#delete_btn").attr("disabled", true);
        }
    }
}