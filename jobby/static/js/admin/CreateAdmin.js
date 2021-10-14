document.addEventListener('DOMContentLoaded', () =>{
  $('.saveAdmin').on('click', function(e){
    var file = document.getElementById('file');
    var ins = file.files.length;
    const xhr = new XMLHttpRequest();
    var csrf_token = document.getElementById('csrf_token').value;
    var form_data = new FormData();

    if (ins > 0 ) {
      var size = file.files[0].size;
      if (size > 2*1024*1024) {
        alert("Picture size is too big! Max 2Mb")
        return false;
      }
    }

    var url = '/adminpanel/create/admin';
    var username = document.getElementById('accountUsername').value;
    var email = document.getElementById('accountEmail').value;
    var full_name = document.getElementById('accountFullName').value;
    var password = document.getElementById('accountPassword').value;
    form_data.append("username", username);
    form_data.append("email", email);
    form_data.append("full_name", full_name);
    form_data.append("password", password);
    form_data.append("file", document.getElementById('file').files[0]);

    if (username.length < 3 || username.length > 50) {
      alert("Username length should be between 3 and 50");
      return false;
    }

    if (email.length < 1 || email.length > 50) {
      alert("Please provide a valid email!");
      return false;
    }

    if (password.length < 6 || password.length > 50) {
      alert("Password length should be between 6 and 50!");
      return false;
    }

    xhr.open('POST', url)
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.onload = () =>{
      if(xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if(result.success){
          saveAdmin(username, email, full_name, result.admin_id);
        }
        else{
          alert(result.msg);
        }
      }
    }
    xhr.send(form_data);
    return false;
  })

  function saveAdmin(username, email, full_name, admin_id){
     var admin_table = document.getElementById('admin_table');
     var form_admin = document.getElementById('form_admin');
     var addAnother = document.getElementById("addAnotherAdmin");
     if (admin_table.style.display == 'none'){
       admin_table.style.display = "";
     }

     var tbody = document.getElementById('tbody_admin');
     tbody.innerHTML += '<tr role="row" class="odd" id=ad_' + admin_id +'>' +
       '<td class="sorting_1">' + username +'</td>' +
       '<td>' + full_name + '</td>' +
       '<td>' + email + '</td>' +
       '<td>' +
         '<a href="/adminpanel/users?user_id=10"><i class="fas fa-edit"></i></a>' +
         '<a class="deleteItem" data="ad_' + admin_id + '" style="cursor: pointer; color: blue;"><i class="fas fa-trash"></i></a>' +
       '</td>' +
     '</tr>';

     form_admin.style.display = 'none';
     addAnother.style.display = "block";
     addAnother.addEventListener('click', function(e){
       form_admin.style.display = "block";
       addAnother.style.display = "none";
     })
     return false;
   }

   document.addEventListener('click', deleteItem);

   function deleteItem(e){
     if (e.target.matches('.deleteItem')){
       const request = new XMLHttpRequest();
       var type_id = $(e.target).attr('data');
       var url = '/deleteItem/' + type_id;

       request.open('GET', url);
       request.onload = () =>{
         if (request.status == 200){
           const result = JSON.parse(request.responseText);
           if(result.success){
             $('#'+type_id).hide('slow', function(){ $('#'+type_id).remove(); });
             tbody = document.getElementById('tbody_admin');
             if (tbody.childElementCount == 0){
               var admin_table = document.getElementById('admin_table');
               admin_table.style.display = "none";
             }
           }
           else{
             alert("Lutfen giriş yapınız");
           }
         }
       }
       request.send();
       return false;
     }
   }

  var readURL = function(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.profile-pic').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
  }

  $(".file-upload").on('change', function(){
      readURL(this);
  });

  $(".upload-button").on('click', function() {
     $(".file-upload").click();
  });

})
