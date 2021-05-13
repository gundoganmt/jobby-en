document.addEventListener('DOMContentLoaded', () => {
  msg = document.getElementsByName('getmessage');
  msg.forEach(function(m){
    m.onclick = () => {
      const request = new XMLHttpRequest();
      var bid_id = parseInt(m.getAttribute('data'));
      var url = '/get-message/' + bid_id;
      request.open('GET', url);

      request.onload = () =>{
        if (request.status == 200){
          const BidData = JSON.parse(request.responseText);
          document.getElementById('preMessage').innerText = BidData.message;
        }
      }
      request.send();
    }
  })
})
