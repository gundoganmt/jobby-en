document.addEventListener('DOMContentLoaded', () =>{
  $('.saveCategory').on('click', function(e){
    var file = document.getElementById('file');
    var ins = file.files.length;
    var category = document.getElementById('category').value;

    if (category.length < 3 || category.length > 150) {
      alert("Category length should be between 3 and 150");
      return false;
    }

    if(ins == 0) {
      alert("Please add an image for this category!")
      return false;
    }

    else {
      var size = file.files[0].size;
      if (size > 2*1024*1024) {
        alert("Picture size is too big! Max 2Mb")
        return false;
      }
    }
  })

  document.addEventListener('click', deleteCat);
  function deleteCat(e){
 		if (e.target.matches('.btn-cat') || e.target.matches('.del-cat')){
      const request = new XMLHttpRequest();
      var type_id = $(e.target).attr('data');
      var url = '/deleteItem/' + type_id;
      request.open('GET', url);

      request.onload = () =>{
        if (request.status == 200){
          const result = JSON.parse(request.responseText);
          if (result.success) {
            var cat_item = document.getElementById(type_id);
            cat_item.parentNode.removeChild(cat_item);
            toastr.success(result.msg, 'Success');
          }
          else {
            Swal.fire({
               icon: 'error',
               title: 'Oops...',
               text: result.msg,
            });
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
