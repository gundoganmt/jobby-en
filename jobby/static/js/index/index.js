document.addEventListener('DOMContentLoaded', () =>{
  $('#bookmark').on('click', function(e){
    const request = new XMLHttpRequest();
    var bookmark_id = parseInt($(this).attr('data'));
    var bookmarkType = parseInt($(this).data('type'));
    if($(this).hasClass('bookmarked')){
      var url = '/unmark/' + bookmark_id;
    }
    else{
      var url = '/bookmark/' + bookmark_id;
    }

    request.open('POST', url);
    request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    request.onload = () =>{
      if (request.status == 200){
        const result = JSON.parse(request.responseText);
        if(result.success){
          if(result.bookmark){
            $(this).html('<i class="uil uil-check"></i> Bookmarked');
            e.preventDefault();
          }
          else {
            $(this).html('<i class="uil uil-bookmark"></i> Bookmark');
            e.preventDefault();
          }
        }
        else{
          alert("Lutfen giriş yapınız");
        }
      }
    }
    request.send(JSON.stringify({"bookmarkType": bookmarkType}));
    return false;
  });

  submitBidButton.addEventListener('click', () =>{
    bid_amount = document.getElementById('bid_amount').value;
    qtyInput = document.getElementById('qtyInput').value;
    qtyOption = document.getElementById('qtyOption').value;
    bidMessage = document.getElementById('bidMessage').value;
    submitBidButton = document.getElementById('submitBidButton');
    
    var form_data = new FormData();
    const xhr = new XMLHttpRequest();
    var url = window.location.pathname;
    var csrf_token = document.getElementById('csrf_token').value;

    form_data.append("bid_amount", bid_amount);
    form_data.append("qtyInput", qtyInput);
    form_data.append("qtyOption", qtyOption);
    form_data.append("bidMessage", bidMessage);

    xhr.open('POST', url)
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.onload = () =>{
      if(xhr.status == 200){
        const result = JSON.parse(xhr.responseText);
        if(result.success){
          window.location.href = result.msg;
        }
      }
    }
    xhr.send(form_data);
    return false;
  })

})
