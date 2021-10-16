function behaviorMapping(){
    return {
        behaviors: [],
        selectedBehavior: 0,
        heading: "",
        description: "",
        behavior: 1,
        impact: 0,
        selectedBehaviors: [],
        feasibility: 0,
        isDeleting: false,
        setValue(propName){
            this[propName] = this.$refs[propName].value;
        },
        resetFields(){
            this.heading = "";
            this.description = "";
            this.behavior = 1;
            this.impact = 0;
            this.feasibility = 0;
            this.selectedBehavior = 0;
            $("#behaviorForm .save-btn").removeClass("d-none");
            $("#behaviorForm .update-btn").addClass("d-none");
            $(".form-col").addClass("d-none");
            $('.form-col-list').removeClass('d-none');
            $(this.$refs.behavior).val(0);
            $(this.$refs.impact).val(0);
            $(this.$refs.feasibility).val(0);
            this.resetErrors();
        },
        addNew(){
            this.resetFields();
            $(".form-col").removeClass("d-none");
            $('.form-col-list').addClass('d-none');
        },
        removeBehavior(i){
            let behavior = this.behaviors[i];
            let box = ".behavior-box[data-impact="+behavior.impact+"][data-feasibility="+behavior.feasibility+"]";

            $(box).html("");
            this.behaviors.splice(i, 1);

            $.ajax({
                type: "POST",
                url: "/behaviour-mapping/delete-behaviour",
                data: {
                    'csrfmiddlewaretoken': T,
                    'data': JSON.stringify(behavior) // from form
                },
                success: function () {
                    console.log('done')
                    location.reload()
                }
            });
            this.behaviors.forEach((ele, index) => {
                if(index >= i){
                    // console.log("");
                    ele.id--;
                    this.behaviors[index] = ele;
                }
            });
            this.isDeleting = true;
            this.resetFields();
        },
        selectBehavior(i){
            if(this.isDeleting){
                this.isDeleting = false;
                this.resetFields();
                return false;
            }
            this.resetErrors();
            this.selectedBehavior = i;
            $("#behaviorForm .save-btn").addClass("d-none");
            $("#behaviorForm .update-btn").removeClass("d-none");
            $(".form-col").removeClass("d-none");
            $('.form-col-list').addClass('d-none');
            this.heading = this.behaviors[i].heading;
            this.description = this.behaviors[i].description;
            this.behavior = this.behaviors[i].behavior;
            this.impact = this.behaviors[i].impact;
            this.feasibility = this.behaviors[i].feasibility;
            $(this.$refs.behavior).val(this.behavior);
            $(this.$refs.impact).val(this.impact);
            $(this.$refs.feasibility).val(this.feasibility);
        },
        addBehavior(){
            // console.log(this.behaviors);
            flag = true;
            this.resetErrors();

            if(!$(this.$refs.behaviorForm).valid()) return false;
            
            // if(this.behavior == 0){
            //    $("#behavior").siblings("span.text-danger").removeClass("d-none");
            //    flag = false;
            // }
            if(this.impact == 0){
                $("#impact").siblings("span.text-danger").removeClass("d-none");
                flag = false;
            }
            if(this.feasibility == 0){
                $("#feasibility").siblings("span.text-danger").removeClass("d-none");
                flag = false;
            }

            let isFound = this.behaviors.find( (behavior) => {
                return (
                    // behavior.behavior == this.behavior &&
                    behavior.impact == this.impact &&
                    behavior.feasibility == this.feasibility
                );
            });
            
            if(typeof isFound === "object"){
                $("span.text-danger.already").removeClass("d-none");
                flag = false;
            }

            if(!flag) return false;
            let id = this.behaviors.length + 1;
            this.behaviors.push({
                id: id,
                heading: this.heading,
                description: this.description,
                behavior: this.behavior,
                impact: parseInt(this.impact),
                feasibility: parseInt(this.feasibility)
            });

            console.log(this.behaviors)
            // send post request using data as 'this.behaviors'

            $.ajax({
                type: "POST",
                url: "/behaviour-mapping/add-behaviour",
                data: {
                    'csrfmiddlewaretoken': T,
                    'data': JSON.stringify(this.behaviors) // from form
                },
                success: function () {
                    console.log('done')
                    location.reload()
                }
            });

            this.mapBehavior(this.behaviors.length - 1);
            $(".form-col").addClass("d-none");
            $('.form-col-list').removeClass('d-none');
            setTimeout(() => this.highlightSelected(), 300);
        },
        updateBehavior(){
            // console.log(this.selectedBehavior);
            flag = true;
            this.resetErrors();

            if(!$(this.$refs.behaviorForm).valid()) return false;
            
            if(this.behavior == 0){
                $("#behavior").siblings("span.text-danger").removeClass("d-none");
                flag = false;
            }
            if(this.impact == 0){
                $("#impact").siblings("span.text-danger").removeClass("d-none");
                flag = false;
            }
            if(this.feasibility == 0){
                $("#feasibility").siblings("span.text-danger").removeClass("d-none");
                flag = false;
            }

            let isFound = this.behaviors.find( (behavior) => {
                console.log(
                    (behavior.id), this.selectedBehavior + 1,
                    behavior.impact, this.impact,
                    behavior.feasibility, this.feasibility
                );
                return (
                    // behavior.behavior == this.behavior &&
                    behavior.impact == this.impact &&
                    behavior.feasibility == this.feasibility
                );
            });
            let behavior = this.behaviors[this.selectedBehavior];
            console.log(isFound, behavior);
            if(typeof isFound === "object" && isFound != behavior){
                $("span.text-danger.already").removeClass("d-none");
                flag = false;
            }

            if(!flag) return false;

            let box = ".behavior-box[data-impact="+behavior.impact+"][data-feasibility="+behavior.feasibility+"]";
            // console.log(box);

            $(box).html("");

            this.behaviors[this.selectedBehavior] = {
                id: behavior.id,
                heading: this.heading,
                description: this.description,
                behavior: parseInt(this.behavior),
                impact: parseInt(this.impact),
                feasibility: parseInt(this.feasibility)
            };
            this.mapBehavior(this.selectedBehavior);

            // send post request using 'this.selectedBehavior'
            $.ajax({
                type: "POST",
                url: "/behaviour-mapping/update-behaviour",
                data: {
                    'csrfmiddlewaretoken': T,
                    'data': JSON.stringify(this.behaviors[this.selectedBehavior]) // from form
                },
                success: function () {
                    console.log('done')
                    location.reload()
                }
            });

            $(".form-col").addClass("d-none");
            $('.form-col-list').removeClass('d-none');
            setTimeout(() => this.highlightSelected(), 300);
        },
        resetErrors(){
            $("#behavior").siblings("span.text-danger").addClass("d-none");
            $("#impact").siblings("span.text-danger").addClass("d-none");
            $("#feasibility").siblings("span.text-danger").addClass("d-none");
            $("span.text-danger.already").addClass("d-none");
        },
        highlightBox(i){
            // console.log($(".card.behavior"));
            // console.log($(".card.behavior.behavior-"+i));
            // $(".card.behavior").removeClass('active');
            // console.log(this.behaviors[i - 1]);                    
            // this.behaviors[i - 1].isSelected = !this.behaviors[i - 1].isSelected;
            // console.log(this.behaviors[i - 1]);                    
            // console.log(this.behaviors);
            if(this.selectedBehaviors.indexOf(i) > -1) this.selectedBehaviors.splice(this.selectedBehaviors.indexOf(i), 1);
            else this.selectedBehaviors.push(i);
            // $(".card.behavior.behavior-"+i).toggleClass('active');
            $(".behavior-heading-"+i).toggleClass("text-bold");
            setTimeout(() => this.highlightSelected(), 300);
        },
        highlightSelected(){
            $(".card.behavior").removeClass('active');
            this.selectedBehaviors.forEach(ele => {
                $(".card.behavior.behavior-"+ele).addClass('active');
            });
        },
        mapBehavior(i){
            let behavior = this.behaviors[i];
            let box = ".behavior-box[data-impact="+behavior.impact+"][data-feasibility="+behavior.feasibility+"]";
            let heading = $("<p class='behavior-heading behavior-heading-"+behavior.id+"' />")
            heading.attr("x-on:click", "highlightBox("+behavior.id+")");
            heading.text(behavior.heading).css('color', (behavior.behavior)?'green':'red'); 
            heading.appendTo(box);
            // console.log(parentClass, box, heading)
        },
        init(){
            fetch('/behaviour-mapping/get-behaviours', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
                body: 'inna'
            })
            .then((response) => response.json())
			.then((data) => {
                var behavior_data = data['data']

				for(let i = 0; i < behavior_data.length; i++){
                    if (behavior_data[i]['fields'].value == '+ve') {
                        var behavior_value = 1
                    }else {
                        var behavior_value = false
                    }
                    this.behaviors.push({
                        id: behavior_data[i]['pk'],
                        heading: behavior_data[i]['fields'].title,
                        description: behavior_data[i]['fields'].description,
                        behavior: behavior_value,
                        impact: behavior_data[i]['fields'].impact,
                        feasibility: behavior_data[i]['fields'].difficulty,
                    });
                    this.mapBehavior(i);

                }

                // make a separate request for this
                for(let i = 0; i < behavior_data.length; i++){
                    if (behavior_data[i]['fields'].is_selected) {
                        var cards = $(".behavior_cards")
                        for(let p = 0; p < cards.length; p++) {
                            if (behavior_data[i]['pk'] == cards[p].id) {
                                alert($(`#${cards[p].id} .behavior_cards`))
                                $(`#${cards[p].id} .behavior_cards`).addClass('active')
                                var pTags = $("p")
                                // for (var i=0; i < cards.length; i++)
                            }
                        }
                    }
                }
			})
        }
    }
}
function randomStr(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) result += characters.charAt(Math.floor(Math.random() * charactersLength));
    return result;
}

function printDiv(divName) {
    $('.round-circle').hide();
    var printContents = document.getElementById(divName).innerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;

    window.print();
       
    document.body.innerHTML = originalContents;
   
   $('.round-circle').show();
       
   }


//
function save() {
        var asp_title = $("#asp_title").val()
        if (asp_title == '') {
            alert('Please write the title of your aspiration before saving')
        } else {
            var cards = $(".behavior_cards.active")
            var id_array = []
            for (var i=0; i < cards.length; i++) {
                id_array.push(cards[i].id)
            }
            $.ajax({
                type: "POST",
                url: "/behaviour-mapping/save-mapping",
                data: {
                    'csrfmiddlewaretoken': T,
                    'data': JSON.stringify(id_array), // from form
                },
                success: function (data, status) {
                    if (status == 'success') {
                        window.location.href = "/members-area";
                    }
                    console.log(status)

                }
            });
        }
    }
