document.addEventListener('DOMContentLoaded', () =>{
  $('.delUser').on('click', function(e){
    const xhr = new XMLHttpRequest();
    var user_id = $(this).attr('data');
    var url = '/delete-user/' + user_id;

    xhr.open('GET', url);
    xhr.onload = () => {
      if (xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if (result.success) {
          $('#'+user_id).hide('slow', function(){ $('#'+user_id).remove(); });
        }
      }
    }
    xhr.send();
  })
})
