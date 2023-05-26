
        $("#project-draft").click(function(){

            $(".project-draft").toggleClass("hide");
  
          });

          $(".sidepanel-dd").click(function(){

                $(".sidepanel-dd-ul").slideToggle();
                $(".dropdown-icon").toggleClass("not-collapse");

          });

    

          var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})



$(document).ready(() => {
  $("#dp_uploaded").hide();
    $("#upload-profile").change(function () {
        const file = this.files[0];
       
        if (file) {
            let reader = new FileReader();
            reader.onload = function (event) {
                $("#dp_uploaded").attr("src", event.target.result);
                $("#dp_uploaded").show();
                $("#toggle_user").remove();
            };
            reader.readAsDataURL(file);

            

        }
    });
});


$("#project-draft").click(function(){

  $(".project-draft").toggleClass(".hide");

});


$("#show-side-navigation").click(function(){


  $("#side-navigation").css("width","250px");

});

$("#hide-side-navigation").click(function(){


  $("#side-navigation").css("width","0");

});