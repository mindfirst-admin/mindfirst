var varCase = {}

varCase.clickCount = 0

$('.swiper-mov').click(function() {
    varCase.clickCount++
    allSlideItems = document.querySelectorAll('.swiper-slide')
    console.log(allSlideItems)

    if (varCase.clickCount == allSlideItems.length-2) {
        setTimeout(function() {
            window.location.href = "/habit-summary";
        }, 2000);
    } else {
        setTimeout(function() {
            varCase.swiperDiv = document.querySelector('.swiper-container').swiper
            varCase.swiperDiv.slideNext();
        }, 2000);
    }
})


$('.swiper-mov2').click(function() {
    varCase.clickCount++
    allSlideItems = document.querySelectorAll('.swiper-slide')
    console.log(allSlideItems)

    if (varCase.clickCount == allSlideItems.length-2) {
        setTimeout(function() {
            window.location.href = "/bad-habit-summary";
        }, 2000);
    } else {
        setTimeout(function() {
            varCase.swiperDiv = document.querySelector('.swiper-container').swiper
            varCase.swiperDiv.slideNext();
        }, 2000);
    }
})


$('.up-btn').click(function(){
    $('#congrats').modal('show');
    $('.modal-backdrop').hide();
    setTimeout(function(){
    if($('#congrats').hasClass('show'))
    {
        console.log($('#congrats').modal('hide'))
            $('#congrats').hide();
            $('.modal-backdrop').hide();
    }
    
    }, 1590);
});
const swiper = new Swiper('.swiper-container', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    navigation: false,
    arrows:false,
    centeredSlides:true,
})


function edit(id) {
    $.ajax({
        type: "POST",
        url: "/characters/go-to-habit",
        data: {
            'behaviors': id // from form
        },
        success: function () {
            console.log('done')
            window.location.href = "/habit-design";
        }
    });
  }

function scale(id) {
    data = {'id': id}

    $.ajax({
        type: "POST",
        url: "/characters/scale-habit",
        data: {
            'data': JSON.stringify(data) // from form
        },
        success: function () {
            console.log('done')
            alert("You just scaled your habit, keep it up you're making great progress. By scaling your habit you get to where you want to be quicker. Well done")
            location.reload()
        }
    });
}