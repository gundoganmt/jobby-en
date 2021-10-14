document.addEventListener('DOMContentLoaded', () =>{
  $('.saveSkill').on('click', function(e){
    var skill = document.getElementById('skill').value;

    if (skill.length < 1 || skill.length > 100) {
      alert("skill length should be between 1 and 100");
      return false;
    }
  })

  document.addEventListener('click', deleteSk);
  function deleteSk(e){
 		if (e.target.matches('.btn-sk') || e.target.matches('.del-sk')){
      const request = new XMLHttpRequest();
      var type_id = $(e.target).attr('data');
      var url = '/deleteItem/' + type_id;
      request.open('GET', url);

      request.onload = () =>{
        if (request.status == 200){
          const result = JSON.parse(request.responseText);
          if (result.success) {
            var sk_item = document.getElementById(type_id);
            sk_item.parentNode.removeChild(sk_item);
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
