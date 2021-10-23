document.addEventListener('DOMContentLoaded', () =>{
  $('.deleteTask').on('click', function(e){
    const xhr = new XMLHttpRequest();
    var task_id = $(this).attr('data');
    var url = '/delete_pro/' + task_id;

    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        xhr.open('GET', url);
        xhr.onload = () => {
          if (xhr.status == 200){
            const result = JSON.parse(xhr.responseText);
            if (result.success) {
              $('#'+task_id).hide('slow', function(){ $('#'+task_id).remove(); });
              Swal.fire(
                'Deleted!',
                result.msg,
                'success'
              )
            }
            else {
              Swal.fire(
                'Error!',
                result.msg,
                'error'
              )
            }
          }
        }
        xhr.send();
      }
    })
  })
})
