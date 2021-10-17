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
   var user_id = $(this).attr('data-user-id');
   var csrf_token = document.getElementById('csrf_token').value;
   var form_data = new FormData();

   if(editProfileType == "personal"){
     var url = '/editUser/personel/' + user_id;
     var username = document.getElementById('accountUsername').value;
     var email = document.getElementById('accountEmail').value;
     var name = document.getElementById('accountFirstName').value;
     var surname = document.getElementById('accountLastName').value;
     var password = document.getElementById('accountPassword').value;
     var phone = document.getElementById('accountPhoneNumber').value;
     form_data.append("username", username);
     form_data.append("email", email);
     form_data.append("name", name);
     form_data.append("surname", surname);
     form_data.append("password", password);
     form_data.append("phone", phone);
     form_data.append("file", document.getElementById('file').files[0]);
   }

   else if(editProfileType == "profile"){
     var url = '/editUser/profile/' + user_id;
     var field_of_work = document.getElementById('field_of_work').value;
     var tagline = document.getElementById('tagline').value;
     var country = document.getElementById('country').value;
     var introduction = document.getElementById('editor-profile').value;
     form_data.append("field_of_work", field_of_work);
     form_data.append("tagline", tagline);
     form_data.append("country", country);
     form_data.append("introduction", introduction);
   }

   else if(editProfileType == "skill"){
     var url = '/editUser/skill/' + user_id;
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
     var url = '/editUser/workexp/' + user_id;
     var position = document.getElementById('position').value;
     var company = document.getElementById('company').value;
     var start_month_job = document.getElementById('start_month_job').value;
     var start_year_job = document.getElementById('start_year_job').value;
     var end_month_job = document.getElementById('end_month_job').value;
     var end_year_job = document.getElementById('end_year_job').value;
     var desc_work = document.getElementById('desc_work').value;

     if (!position || position.length > 150) {
       alert("Please provide valid position!");
       return false;
     }

     if (!company || company.length > 150) {
       alert("Please provide valid company!");
       return false;
     }

     form_data.append("position", position);
     form_data.append("company", company);
     form_data.append("start_month_job", start_month_job);
     form_data.append("start_year_job", start_year_job);
     form_data.append("end_month_job", end_month_job);
     form_data.append("end_year_job", end_year_job);
     form_data.append("desc_work", desc_work);
   }

   else if(editProfileType == "education"){
     var url = '/editUser/education/' + user_id;
     var field = document.getElementById('field').value;
     var school = document.getElementById('school').value;
     var start_month_edu = document.getElementById('start_month_edu').value;
     var start_year_edu = document.getElementById('start_year_edu').value;
     var end_month_edu = document.getElementById('end_month_edu').value;
     var end_year_edu = document.getElementById('end_year_edu').value;
     var desc_edu = document.getElementById('desc_edu').value;

     if (!field || field.length > 150) {
       alert("Please provide valid field of study!");
       return false;
     }

     if (!school || school.length > 150) {
       alert("Please provide valid school name!");
       return false;
     }

     form_data.append("field", field);
     form_data.append("school", school);
     form_data.append("start_month_edu", start_month_edu);
     form_data.append("start_year_edu", start_year_edu);
     form_data.append("end_month_edu", end_month_edu);
     form_data.append("end_year_edu", end_year_edu);
     form_data.append("desc_edu", desc_edu);
   }

   else if (editProfileType == "social"){
     var url = '/editUser/social/' + user_id;
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
           saveWorkExp(result.position, result.company, result.workExp_id, result.duration);
         }
         else if(result.editProfileType == 'pro'){
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
           saveEdu(result.field, result.school, result.edu_id, result.duration);
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
       }
       else{
         alert(result.msg);
       }
     }
   }
   xhr.send(form_data);
   return false;
  })

  function saveSkill(skill, level, skill_id){
     var skill_table = document.getElementById('skill_table');
     var form_skill = document.getElementById('form_skill');
     var addAnother = document.getElementById("addAnotherSkill");
     if (skill_table.style.display == 'none'){
       skill_table.style.display = "";
     }

     var tbody = document.getElementById('tbody_skill');
     tbody.innerHTML += '<tr role="row" class="odd" id=s_' + skill_id + '>' +
       '<td class="sorting_1">' + skill +'</td>' +
       '<td>' + level + '</td>' +
       '<td>' +
         '<a class="deleteItem" data="s_' + skill_id + '" style="cursor: pointer; color: blue;"><i class="fas fa-trash deleteItem" data="s_' + skill_id + '"></i></a>' +
       '</td>' +
     '</tr>';

     form_skill.style.display = 'none';
     addAnother.style.display = "block";
     addAnother.addEventListener('click', function(e){
       form_skill.style.display = "block";
       addAnother.style.display = "none";
     })
     return false;
   }

  function saveWorkExp(position, company, workExp_id, duration){
    var workExp_table = document.getElementById('workExp_table');
    var form_workexp = document.getElementById('form_workexp');
    var addAnother = document.getElementById("addAnotherWorkexp");
    if (workExp_table.style.display == 'none'){
      workExp_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_work');
    tbody.innerHTML += '<tr role="row" class="odd" id=w_' + workExp_id + '>' +
      '<td class="sorting_1">' + position +'</td>' +
      '<td>' + company + '</td>' +
      '<td>' + duration + '</td>' +
      '<td>' +
        '<a class="deleteItem" data="w_' + workExp_id + '" style="cursor: pointer; color: blue;"><i class="fas fa-trash deleteItem" data="w_' + workExp_id + '"></i></a>' +
      '</td>' +
    '</tr>';

    form_workexp.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_workexp.style.display = "block";
      addAnother.style.display = "none";
    })
    return false;
  }

  function saveEdu(field, school, edu_id, duration){
    var edu_table = document.getElementById('edu_table');
    var form_edu = document.getElementById('form_edu');
    var addAnother = document.getElementById("addAnotherEdu");
    if (edu_table.style.display == 'none'){
      edu_table.style.display = "";
    }

    var tbody = document.getElementById('tbody_edu');
    tbody.innerHTML += '<tr role="row" class="odd" id=e_' + edu_id + '>' +
      '<td class="sorting_1">' + field +'</td>' +
      '<td>' + school + '</td>' +
      '<td>' + duration + '</td>' +
      '<td>' +
        '<a class="deleteItem" data="e_' + edu_id + '" style="cursor: pointer; color: blue;"><i class="fas fa-trash deleteItem" data="e_' + edu_id + '"></i></a>' +
      '</td>' +
    '</tr>';

    form_edu.style.display = 'none';
    addAnother.style.display = "block";
    addAnother.addEventListener('click', function(e){
      form_edu.style.display = "block";
      addAnother.style.display = "none";
    })
    return false;
  }

 document.addEventListener('click', deleteItem);

 function deleteItem(e){
   if (e.target.matches('.deleteItem')){
     const request = new XMLHttpRequest();
     var type_id = $(e.target).attr('data');
     var url = '/deleteItem/' + type_id;

     request.open('GET', url);
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
             var tbody = document.getElementById('tbody_work');
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
           alert("Lutfen giriş yapınız");
         }
       }
     }
     request.send();
     return false;
   }
 }

})
