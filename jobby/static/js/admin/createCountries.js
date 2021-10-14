document.addEventListener('DOMContentLoaded', () =>{
  $('.saveCountry').on('click', function(e){
    var country = document.getElementById('country').value;

    if (country.length < 2 || country.length > 100) {
      alert("Country length should be between 2 and 100");
      return false;
    }
  })

  document.addEventListener('click', deleteCtr);
  function deleteCtr(e){
 		if (e.target.matches('.btn-ctr') || e.target.matches('.del-ctr')){
      const request = new XMLHttpRequest();
      var type_id = $(e.target).attr('data');
      var url = '/deleteItem/' + type_id;
      request.open('GET', url);

      request.onload = () =>{
        if (request.status == 200){
          const result = JSON.parse(request.responseText);
          if (result.success) {
            var ctr_item = document.getElementById(type_id);
            ctr_item.parentNode.removeChild(ctr_item);
          }
          else {
            alert(result.msg)
          }
        }
      }
      request.send();
      return false;
    }
  }

})
