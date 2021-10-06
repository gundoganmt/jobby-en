document.addEventListener('DOMContentLoaded', () =>{
  $('.saveCategory').on('click', function(e){
    const xhr = new XMLHttpRequest();
    var csrf_token = document.getElementById('csrf_token').value;
    var url = '/adminpanel/create/categories';
    var form_data = new FormData();
    var category = document.getElementById('category').value;
    form_data.append("category", category);

    xhr.open('POST', url)
   	xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.onload = () => {
      if (xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if (result.success) {
          console.log("success");
          var catlist = document.getElementById('catlist');
          if (catlist.style.display == 'none') {
            catlist.style.display = '';
          }
          console.log("here");
          catlist.innerHTML += '<div class="col-md-10">' +
            '<input type="text" readonly="" class="form-control" value="' + category + '">' +
          '</div>' +
          '<div class="col-md-2">' +
            '<button type="button"  class="btn btn-danger">Delete</button>' +
          '</div>';
        }
        else {
          alert(result.msg);
        }
      }
    }
    xhr.send(form_data);
  })
})
