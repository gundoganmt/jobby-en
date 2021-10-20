 document.addEventListener('DOMContentLoaded', () => {
   $('.collapse').on('click', function(e){
     if($(this).next().css("display") == 'none'){
       $(this).next().show();
     }
     else {
       $(this).next().hide();
     }
   })

   //if a record exist then only show that otherwise show form
   list_group = document.getElementsByClassName('list-group');
   for (ls of list_group){
     var li = ls.firstElementChild;
     if(li.style.display != 'none'){
       ls.parentNode.nextElementSibling.style.display = 'none';
     }
   }

   $('.saveSetting').on('click', function(e){
   	const xhr = new XMLHttpRequest();
   	var editProfileType = $(this).attr('data');
   	var csrf_token = document.getElementById('csrf_token').value;
    var form_data = new FormData();

    if(editProfileType == "personal"){
      var url = '/editProfile/personal';
      var username = document.getElementById('username').value;
      var email = document.getElementById('email').value;
      var name = document.getElementById('firstName').value;
      var surname = document.getElementById('surname').value;
      form_data.append("username", username);
      form_data.append("email", email);
      form_data.append("name", name);
      form_data.append("surname", surname);
      form_data.append("file", document.getElementById('file').files[0]);
    }

   	if(editProfileType == "profile"){
   		var url = '/editProfile/profile';
      var editor = document.querySelector('#editor3');
   		var field_of_work = document.getElementById('field_of_work').value;
   		var tagline = document.getElementById('tagline').value;
   		var location = document.getElementById('location').value;
   		var introduction = document.querySelector('#profileQuill');
      introduction.value = editor.children[0].innerHTML;
      form_data.append("field_of_work", field_of_work);
      form_data.append("tagline", tagline);
      form_data.append("location", location);
      form_data.append("introduction", introduction.value);
   	}

   	else if(editProfileType == "skill"){
   		var url = '/editProfile/skill';
   		var skill = document.getElementById('skill').value;
   		var level = document.getElementById('level').value;
      if (parseInt(level) > 100 || parseInt(level) < 0 || !level) {
        alert("level should be a number between 0 and 100");
        return false;
      }

      if (!skill || skill.length > 50) {
        alert("skill length should be between 0 and 100");
        return false;
      }
      form_data.append("skill", skill);
      form_data.append("level", level);
   	}

   	else if(editProfileType == "workExp"){
      var url = '/editProfile/workExp';
      var editor = document.querySelector('#editor2');
      var position = document.getElementById('position').value;
      var company = document.getElementById('company').value;
      var start_month_job = document.getElementById('start_month_job').value;
      var start_year_job = document.getElementById('start_year_job').value;
      var end_month_job = document.getElementById('end_month_job').value;
      var end_year_job = document.getElementById('end_year_job').value;
      var desc_work = document.querySelector('#desc_work');
      desc_work.value = editor.children[0].innerHTML;
      form_data.append("position", position);
      form_data.append("company", company);
      form_data.append("start_month_job", start_month_job);
      form_data.append("start_year_job", start_year_job);
      form_data.append("end_month_job", end_month_job);
      form_data.append("end_year_job", end_year_job);
      form_data.append("desc_work", desc_work.value);
   	}

   	else if(editProfileType == "education"){
      var url = '/editProfile/education';
      var editor = document.querySelector('#editor');
      var field = document.getElementById('field').value;
      var school = document.getElementById('school').value;
      var start_month_edu = document.getElementById('start_month_edu').value;
      var start_year_edu = document.getElementById('start_year_edu').value;
      var end_month_edu = document.getElementById('end_month_edu').value;
      var end_year_edu = document.getElementById('end_year_edu').value;
      var desc_edu = document.querySelector('#desc_edu');
      desc_edu.value = editor.children[0].innerHTML;
      form_data.append("field", field);
      form_data.append("school", school);
      form_data.append("start_month_edu", start_month_edu);
      form_data.append("start_year_edu", start_year_edu);
      form_data.append("end_month_edu", end_month_edu);
      form_data.append("end_year_edu", end_year_edu);
      form_data.append("desc_edu", desc_edu.value);
   	}

    else if (editProfileType == "social"){
   		var url = '/editProfile/social';
   		var facebook = document.getElementById('facebook').value;
   		var twitter = document.getElementById('twitter').value;
   		var youtube = document.getElementById('youtube').value;
      var github = document.getElementById('github').value;
   		var instagram = document.getElementById('instagram').value;
   		var linkedin = document.getElementById('linkedin').value;
      form_data.append("facebook", facebook);
      form_data.append("twitter", twitter);
      form_data.append("youtube", youtube);
      form_data.append("github", github);
      form_data.append("instagram", instagram);
      form_data.append("linkedin", linkedin);
   	}

   	xhr.open('POST', url)
   	xhr.setRequestHeader("X-CSRFToken", csrf_token);
   	xhr.onload = () =>{
   		if(xhr.status == 200){
   			const result = JSON.parse(xhr.responseText);
   			if(result.success){
          if(result.editProfileType == 's'){
            saveSkill(result.skill,result.level, result.skill_id);
          }
          else if(result.editProfileType == 'w'){
            saveWorkExp(result.workExp, result.company, result.workExp_id);
          }
          else if(result.editProfileType == 'so'){
            Swal.fire({
              icon: 'success',
              title: "Good job!",
              text: "Saved successfully!",
              type: "success",
              confirmButtonClass: 'btn btn-primary',
              buttonsStyling: false,
            });
          }
          else if(result.editProfileType == 'per'){
            Swal.fire({
              icon: 'success',
              title: "Good job!",
              text: "Saved successfully!",
              type: "success",
              confirmButtonClass: 'btn btn-primary',
              buttonsStyling: false,
            });
          }
          else if(result.editProfileType == 'e'){
            saveEdu(result.field, result.school, result.edu_id);
          }
          else if(result.editProfileType == 'p'){
            Swal.fire({
              icon: 'success',
              title: "Good job!",
              text: "Saved successfully!",
              type: "success",
              confirmButtonClass: 'btn btn-primary',
              buttonsStyling: false,
            });
          }
   			}
   			else{
          Swal.fire({
             icon: 'error',
             title: 'Oops...',
             text: result.msg,
          });
   			}
   		}
   	}
   	xhr.send(form_data);
   	return false;
   })

   function saveSkill(skill, level, skill_id){
      var skill_table = document.getElementById('skill_table');
      var form_skill = document.getElementById('skillForm');
      if (skill_table.style.display == 'none'){
        skill_table.style.display = "";
      }

      var tbody = document.getElementById('tbody_skill');
      tbody.innerHTML += '<tr class="table-active" id=s_' + skill_id + '>' +
        '<td>' +
          '<span class="font-weight-bold">' + skill + '</span>' +
        '</td>' +
        '<td>' + level + '</td>' +
        '<td>' +
        '<button type="button" class="btn btn-danger deleteItem" data="s_' + skill_id + '"><i class="icon-feather-trash-2"></i></button>' +
        '</td>' +
      '</tr>';

      form_skill.style.display = 'none';
      return false;
    }

   function saveWorkExp(position, company, workExp_id){
     var workExp_table = document.getElementById('workExp_table');
     var form_workexp = document.getElementById('workExpForm');
     if (workExp_table.style.display == 'none'){
       workExp_table.style.display = "";
     }

     var tbody = document.getElementById('tbody_workExp');
     tbody.innerHTML += '<tr class="table-active" id=w_' + workExp_id + '>' +
       '<td>' +
         '<span class="font-weight-bold">' + position + '</span>' +
       '</td>' +
       '<td>' + company + '</td>' +
       '<td>' +
       '<button type="button" class="btn btn-danger deleteItem" data="w_' + workExp_id + '"><i class="icon-feather-trash-2"></i></button>' +
       '</td>' +
     '</tr>';

     form_workexp.style.display = 'none';
     return false;
   }

   function saveEdu(field, school, edu_id){
     var edu_table = document.getElementById('edu_table');
     var form_edu = document.getElementById('eduForm');
     if (edu_table.style.display == 'none'){
       edu_table.style.display = "";
     }

     var tbody = document.getElementById('tbody_edu');
     tbody.innerHTML += '<tr class="table-active" id=e_' + edu_id + '>' +
       '<td>' +
         '<span class="font-weight-bold">' + field + '</span>' +
       '</td>' +
       '<td>' + school + '</td>' +
       '<td>' +
       '<button type="button" class="btn btn-danger deleteItem" data="e_' + edu_id + '"><i class="icon-feather-trash-2"></i></button>' +
       '</td>' +
     '</tr>';

     form_edu.style.display = 'none';
     return false;
   }

  document.addEventListener('click', deleteItem);

  function deleteItem(e){
 		if (e.target.matches('.deleteItem')){
      const request = new XMLHttpRequest();
      var csrf_token = document.getElementById('csrf_token').value;
   		var type_id = $(e.target).attr('data');
      var form_data = new FormData()
      form_data.append('type_id', type_id);
   		var url = '/deleteItem';

      request.open('POST', url);
     	request.setRequestHeader("X-CSRFToken", csrf_token);
  		request.onload = () =>{
  			if (request.status == 200){
  				const result = JSON.parse(request.responseText);
  				if(result.success){
            if (result.currentField == 's') {
              var tbody = document.getElementById('tbody_skill');
              var item = document.getElementById(type_id);
              item.parentNode.removeChild(item);
              if (tbody.childElementCount == 0){
                var skill_table = document.getElementById('skill_table');
                skill_table.style.display = "none";
              }
              e.preventDefault();
            }
            else if (result.currentField == 'w') {
              var tbody = document.getElementById('tbody_workExp');
              var item = document.getElementById(type_id);
              item.parentNode.removeChild(item);
              if (tbody.childElementCount == 0){
                var workExp_table = document.getElementById('workExp_table');
                workExp_table.style.display = "none";
              }
              e.preventDefault();
            }
            else if (result.currentField == 'e') {
              var tbody = document.getElementById('tbody_edu');
              var item = document.getElementById(type_id);
              item.parentNode.removeChild(item);
              if (tbody.childElementCount == 0){
                var edu_table = document.getElementById('edu_table');
                edu_table.style.display = "none";
              }
              e.preventDefault();
            }
  				}
  				else{
            Swal.fire({
               icon: 'error',
               title: 'Oops...',
               text: result.msg,
            });
  				}
  			}
  		}
  		request.send(form_data);
  		return false;
    }
  }

  addButton = document.getElementsByName('addButton');
  addButton.forEach(function(btn){
    btn.onclick = () =>{
      var row = btn.previousElementSibling;
      if(row.style.display == 'none'){
        row.style.display = '';
      }
      else{
        alert("Please save the open form first!");
      }
    }
  })

 })
