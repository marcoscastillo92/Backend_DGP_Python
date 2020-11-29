function searchAlumnos() {
    // Declare variables
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('myInputAlumnos');
    filter = input.value.toUpperCase();
    ul = document.getElementById("alumnos");
    li = ul.getElementsByTagName("option")
   
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }

  function searchMiembros() {
    // Declare variables
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('myInputMiembros');
    filter = input.value.toUpperCase();
    ul = document.getElementById("miembros");
    li = ul.getElementsByTagName("option")
   
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }


    function addUser() {
        var sAlumnos = document.getElementById('alumnos')
        var sMiembros = document.getElementById('miembros')
        for ( var i = 0, len = sAlumnos.options.length; i < len; i++ ) {
            opt = sAlumnos.options[i];
            if ( opt && opt.selected === true ) {
                console.log(opt)
                nodo = opt.cloneNode()
                nodo.selected = false
                nodo.value = opt.value
                nodo.innerHTML = opt.innerHTML
                sAlumnos.remove(i)
                console.log(nodo)
                sMiembros.appendChild(nodo)
            }
        }
    }

    function removeUser() {
        var sAlumnos = document.getElementById('alumnos')
        var sMiembros = document.getElementById('miembros')
        for ( var i = 0, len = sMiembros.options.length; i < len; i++ ) {
            opt = sMiembros.options[i];
            if ( opt && opt.selected === true ) {
                console.log(opt)
                nodo = opt.cloneNode()
                nodo.selected = false
                nodo.value = opt.value
                nodo.innerHTML = opt.innerHTML
                sMiembros.remove(i)
                console.log(nodo)
                sAlumnos.appendChild(nodo)
            }
        }
    }

    function selectMiembrosItems() {
      var sMiembros = document.getElementById('miembros')
      for ( var i = 0, len = sMiembros.options.length; i < len; i++ ) {
          opt = sMiembros.options[i];
          opt.selected = true
      }
  }


