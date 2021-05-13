 document.addEventListener('DOMContentLoaded', () => {
   headline = document.getElementsByName('collapse');
   headline.forEach(function(h){
     h.onclick = () =>{
       if (h.offsetParent.lastElementChild.style.display == 'none'){
         h.offsetParent.lastElementChild.style.display = 'block';
       }
       else{
         h.offsetParent.lastElementChild.style.display = 'none';
       }
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
   	var settingType = $(this).attr('data');
   	var csrf_token = document.getElementById('csrf_token').value;

   	if(settingType == "profile"){
   		var url = '/setting/profile';
      var editor = document.querySelector('#editor3');
   		var field_of_work = document.getElementById('field_of_work');
   		var tagline = document.getElementById('tagline');
   		var province = document.getElementById('province');
   		var introduction = document.querySelector('#profileQuill');
      introduction.value = editor.children[0].innerHTML;
   		var data = {'field_of_work': field_of_work.value, "tagline": tagline.value,
   		'province': province.value, "introduction": introduction.value};
   	}

   	else if(settingType == "skill"){
   		var url = '/setting/skill';
   		var skill = document.getElementById('skill').value;
   		var level = document.getElementById('level').value;
   		var data = {'skill': skill, "level": level};
   	}

   	else if(settingType == "workExp"){
      var url = '/setting/workExp';
      var editor = document.querySelector('#editor2');
      var position = document.getElementById('position').value;
      var company = document.getElementById('company').value;
      var start_month_job = document.getElementById('start_month_job').value;
      var start_year_job = document.getElementById('start_year_job').value;
      var end_month_job = document.getElementById('end_month_job').value;
      var end_year_job = document.getElementById('end_year_job').value;
      var desc_work = document.querySelector('#desc_work');
      desc_work.value = editor.children[0].innerHTML;
      var data = {'position': position, "company": company, "start_month_job": start_month_job,
      "start_year_job": start_year_job, "end_month_job": end_month_job, "end_year_job": end_year_job,
      "desc_work": desc_work.value};
   	}

   	else if(settingType == "education"){
      var url = '/setting/education';
      var editor = document.querySelector('#editor');
      var field = document.getElementById('field').value;
      var school = document.getElementById('school').value;
      var start_month_edu = document.getElementById('start_month_edu').value;
      var start_year_edu = document.getElementById('start_year_edu').value;
      var end_month_edu = document.getElementById('end_month_edu').value;
      var end_year_edu = document.getElementById('end_year_edu').value;
      var desc_edu = document.querySelector('#desc_edu');
      desc_edu.value = editor.children[0].innerHTML;
      var data = {'field': field, "school": school, "start_month_edu": start_month_edu,
      "start_year_edu": start_year_edu, "end_month_edu": end_month_edu, "end_year_edu": end_year_edu,
      "desc_edu": desc_edu.value};
   	}

   	else if (settingType == "security"){
   		var url = '/setting/security';
   		var password = document.getElementById('password');
   		var new_password = document.getElementById('new_password');
   		var confirm_password = document.getElementById('confirm_password');
   		var data = {'password': password.value, "new_password": new_password.value, "confirm_password": confirm_password.value};
   	}

   	xhr.open('POST', url)
   	xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
   	xhr.setRequestHeader("X-CSRFToken", csrf_token);
   	xhr.onload = () =>{
   		if(xhr.status == 200){
   			const result = JSON.parse(xhr.responseText);
   			if(result.success){
          if(result.settingType == 's'){
            saveSkill(result.skill, result.skill_id);
          }
          else if(result.settingType == 'w'){
            saveWorkExp(result.workExp, result.workExp_id);
          }
          else if(result.settingType == 'e'){
            saveEdu(result.edu, result.edu_id);
          }
          else if(result.settingType == 'p'){
            alert(result.msg);
          }

   			}
   			else{
   				alert(result.msg);
   			}
   		}
   	}
   	xhr.send(JSON.stringify(data));
   	return false;
   })

   function saveSkill(skill, skill_id){
     var parent = document.getElementById('skill_ul');
     var li = parent.firstElementChild.cloneNode(true);
     var form = document.getElementById('skillForm');
     li.firstElementChild.innerText = skill;
     li.style.display = "block";
     li.setAttribute('id', "s_"+skill_id);
     li.lastElementChild.lastElementChild.setAttribute('data', "s_"+skill_id);
     parent.appendChild(li);
     form.style.display = 'none';
   }

   function saveWorkExp(workExp, workExp_id){
     var parent = document.getElementById('workExp_ul');
     var li = parent.firstElementChild.cloneNode(true);
     var form = document.getElementById('workExpForm');
     li.firstElementChild.innerText = workExp;
     li.style.display = "block";
     li.setAttribute('data', "w_"+workExp_id);
     li.lastElementChild.lastElementChild.setAttribute('data', "w_"+workExp_id);
     parent.appendChild(li);
     form.style.display = 'none';
   }

   function saveEdu(edu, edu_id){
     var parent = document.getElementById('edu_ul');
     var li = parent.firstElementChild.cloneNode(true);
     var form = document.getElementById('eduForm');
     li.firstElementChild.innerText = edu;
     li.style.display = "block";
     li.setAttribute('data', "w_"+edu_id);
     li.lastElementChild.lastElementChild.setAttribute('data', "w_"+edu_id);
     parent.appendChild(li);
     form.style.display = 'none';
   }

  document.addEventListener('click', deleteItem);

  function deleteItem(e){
 		if (e.target.matches('.deleteItem')){
      const request = new XMLHttpRequest();
      var csrf_token = document.getElementById('csrf_token').value;
   		var type_id = $(e.target).attr('data');
      var data = {"type_id": type_id};
   		var url = '/deleteItem';

      request.open('POST', url);
      request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
     	request.setRequestHeader("X-CSRFToken", csrf_token);
  		request.onload = () =>{
  			if (request.status == 200){
  				const result = JSON.parse(request.responseText);
  				if(result.success){
            var item = document.getElementById(type_id);
  					item.parentNode.removeChild(item);
  					e.preventDefault();
  				}
  				else{
  					alert("Lutfen giriş yapınız");
  				}
  			}
  		}
  		request.send(JSON.stringify(data));
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
        alert("Lutfen açık formu kaydedin");
      }
    }
  })

  $('.list_group-item').on('click', function(e){

  })

 })
