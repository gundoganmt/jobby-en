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
 		if (e.target.matches('.btn-ctr') || e.target.matches('.del-ctr')){
      const request = new XMLHttpRequest();
      var ctr_id = $(e.target).attr('data');
      var url = '/del-sk/' + ctr_id;
      request.open('GET', url);

      request.onload = () =>{
        if (request.status == 200){
          const result = JSON.parse(request.responseText);
          if (result.success) {
            var ctr_item = document.getElementById(ctr_id);
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
