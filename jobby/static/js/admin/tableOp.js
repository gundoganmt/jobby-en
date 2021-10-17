document.addEventListener('DOMContentLoaded', () =>{
  $('.deleteItem').on('click', function(e){
    const xhr = new XMLHttpRequest();
    var type_id = $(this).attr('data');
    var url = '/deleteItem/' + type_id;

    xhr.open('GET', url);
    xhr.onload = () => {
      if (xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if (result.success) {
          $('#'+type_id).hide('slow', function(){ $('#'+type_id).remove(); });
        }
      }
    }
    xhr.send();
  })
})
