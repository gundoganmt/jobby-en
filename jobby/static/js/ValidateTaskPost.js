var send_post = document.getElementById('send_post');

function createErrField(error){
  content = document.getElementById('content');
  errmsg = document.createElement('div');
  errmsg.setAttribute('class', "notification error closeable");
  pInner = document.createElement('p');
  pInner.innerText = error;
  aInner = document.createElement('a');
  aInner.setAttribute('class', 'close');
  aInner.setAttribute('href', '#');
  errmsg.appendChild(aInner);
  errmsg.appendChild(pInner);
  content.insertBefore(errmsg, content.firstChild);
}

document.addEventListener('DOMContentLoaded', () =>{
  send_post.addEventListener('click', (e) =>{
    c = document.getElementsByClassName("closeable");
    for (let item of c){
      item.style.display='none';
    }

    var project_name = document.getElementById('project_name').value;
    var category = document.getElementById('category').value;
    var location = document.getElementById('location').value;
    var budget_min = document.getElementById('budget_min').value;
    var budget_max = document.getElementById('budget_max').value;
    var description = document.getElementById('description');
    var editor = document.querySelector('#editor');
    var description = editor.children[0].innerHTML;
    var skills_list = $('#skills').val();

    if (skills_list.length == 0){
      createErrField("Add at least 1 skills!");
      send_post.innerHTML = 'Post Project';
      send_post.disabled = false;
      e.preventDefault();
    }

    if (project_name.length < 5){
      createErrField("Project name is too short");
      send_post.innerHTML = 'Post Project';
      send_post.disabled = false;
      e.preventDefault();
    }

    if (!category){
      createErrField("Please choose a category!");
      send_post.innerHTML = 'Post Project';
      send_post.disabled = false;
      e.preventDefault();
    }
    if (!location){
      createErrField("Please enter a location!");
      send_post.innerHTML = 'Post Project';
      send_post.disabled = false;
      e.preventDefault();
    }
    if (parseInt(budget_min) > parseInt(budget_max)){
      createErrField("Minimum budget cannot exceed maximum budget!");
      send_post.innerHTML = 'Post Project';
      send_post.disabled = false;
      e.preventDefault();
    }
    if (description.length < 30){
      createErrField("Please explain your project. At least 30 character.");
      send_post.innerHTML = 'Post Project';
      send_post.disabled = false;
      e.preventDefault();
    }
    else {
      var task_id = send_post.getAttribute('data');
      if (task_id != "postpro") {
        var url = '/edittask/' + task_id;
      }
      else {
        var url = '/posttask';
        var ins = document.getElementById('upload').files.length;

        if(ins != 0) {
          var size = document.getElementById('upload').files[0].size;
          if (size > 2*1024*1024) {
            alert("Picture size is too big! Max 2Mb")
            send_post.innerHTML = 'Post Project';
            send_post.disabled = false;
            e.preventDefault();
            return false;
          }
        }
        else {
          alert("Please add relevant image to your project")
          send_post.innerHTML = 'Post Project';
          send_post.disabled = false;
          e.preventDefault();
          return false;
        }
      }

      var csrf_token = document.getElementById('csrf_token').value;
      const xhr = new XMLHttpRequest();
      var form_data = new FormData();

      form_data.append("project_name", project_name);
      form_data.append("category", category);
      form_data.append("location", location);
      form_data.append("budget_min", budget_min);
      form_data.append("budget_max", budget_max);
      form_data.append("skills_list", skills_list);
      form_data.append("description", description);
      form_data.append("file", document.getElementById('upload').files[0]);
      send_post.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Posting';
      send_post.disabled = true;

      xhr.open('POST', url)
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
      xhr.onload = () =>{
        if(xhr.status == 200){
          const result = JSON.parse(xhr.responseText);
          if(result.success){
            window.location.href = result.msg;
          }
          else {
            alert(result.msg);
            send_post.innerHTML = 'Post Project';
            send_post.disabled = false;
          }
        }
      }
      xhr.send(form_data);
      return false;
    }
    send_post.innerHTML = 'Post Project';
    send_post.disabled = false;
  })

})
