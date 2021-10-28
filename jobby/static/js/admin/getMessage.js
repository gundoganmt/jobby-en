document.addEventListener('DOMContentLoaded', () => {
  var msg = document.getElementsByName('getmessage');
  msg.forEach(function(m){
    m.onclick = () => {
      const request = new XMLHttpRequest();
      var con_id = parseInt(m.getAttribute('data'));
      var url = '/get-con-message/' + con_id;
      request.open('GET', url);

      if(request.readyState){
        document.getElementById('content').innerText = "";
      }

      request.onload = () =>{
        if (request.status == 200){
          const con_data = JSON.parse(request.responseText);
          if(con_data.success){
            document.getElementById('content').innerText = con_data.msg;
            document.getElementById('conSubject').innerText = con_data.subject;
          }
          else {
            document.getElementById('content').innerText = con_data.msg;
          }
        }
      }

      request.onerror = () =>{
        document.getElementById('content').innerText = "Some thing went wrong! Refresh page and try again.";
      }
      request.send();
    }
  })

  var rply = document.getElementsByName('replyMessage');
  rply.forEach(function(r){
    r.onclick = () => {
      var con_id = parseInt(r.getAttribute('data'));
      var url = '/reply-contact/' + con_id;
      $('#replyForm').attr('action', url);
    }
  })

})
