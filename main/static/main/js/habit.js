var varCase = {}

varCase.clickCount = 0

$('.swiper-mov').click(function() {
    varCase.clickCount++
    allSlideItems = document.querySelectorAll('.swiper-slide')
    console.log(allSlideItems)

    if (varCase.clickCount == allSlideItems.length-2) {
        setTimeout(function() {
            window.location.href = "/behaviour-mapping/habit-summary/positive/";
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
            window.location.href = "/behaviour-mapping/habit-summary/negative";
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

function scale(id) {
    data = {'id': id}

    $.ajax({
        type: "POST",
        url: "/behaviour-mapping/scale-habit",
        data: {
            'csrfmiddlewaretoken': T,
            'data': JSON.stringify(data) // from form
        },
        success: function () {
            console.log('done')
            alert("You just scaled your habit, keep it up you're making great progress. By scaling your habit you get to where you want to be quicker. Well done")
            location.reload()
        }
    });
}

function delete_id(id) {
    data = {'id': id}

    $.ajax({
      type: "POST",
      url: "/behaviour-mapping/delete-behaviour",
      data: {
          'csrfmiddlewaretoken': T,
          'data': JSON.stringify(data) // from form
      },
      success: function () {
          console.log('done')
          window.location.href = "/members-area";
      }
    });
  }

function thumbsUp(id) {
  // thumbs up
  $.ajax({
      type: "POST",
      url: "/behaviour-mapping/record-todays-habit",
      data: {
          'csrfmiddlewaretoken': T,
          'thumbsUp': id
      },
      success: function () {
          console.log('done')
      }
  });
}

function thumbsDown (id) {
  // thumbs down
  $.ajax({
      type: "POST",
      url: "/behaviour-mapping/record-todays-habit",
      data: {
          'csrfmiddlewaretoken': T,
          'thumbsDown': id
      },
      success: function () {
          console.log('done')
      }
  });
}