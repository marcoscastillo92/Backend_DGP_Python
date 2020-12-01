$(document).on("click", ".deleteGroup", function () {
  var name = $(this).data('name');
  var createdAt = $(this).data('created');
  var participants = $(this).data('participants');
  var id = $(this).data('id');
  $(".modal-body #recipient-name").val( name );
  $(".modal-body #recipient-createdAt").val( createdAt );
  $(".modal-body #recipient-memberCount").val( participants );
  $(".modal-body #recipient-id").val( id );
});

$(document).on("click", ".groupMemeber", function () {
  var idGroup = $(this).data('identifier');
  var url = "http://localhost:8000/tutors/groups/get/"
  $.ajax({
    url: url.concat(idGroup),
    type: 'GET',
    success: function(res) {

    }
  });
});

function myFunction() {
    // Declare variables
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByClassName("fila")
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("h5")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }

 