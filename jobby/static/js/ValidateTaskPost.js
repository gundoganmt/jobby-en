var form = document.getElementById('post_job');
form.addEventListener('submit', validate);

function createErrField(error){
  errmsg = document.createElement('div');
  errmsg.setAttribute('class', "notification error closeable");
  pInner = document.createElement('p');
  pInner.innerText = error;
  aInner = document.createElement('a');
  aInner.setAttribute('class', 'close');
  aInner.setAttribute('href', '#');
  errmsg.appendChild(aInner);
  errmsg.appendChild(pInner);
}

function validate(e){

  var job_name = form.job_name.value;
  var category = form.category.value;
  var salary_min = parseInt(form.salary_min.value);
  var salary_max = parseInt(form.salary_max.value);
	var description = form.description.value;
  var skills = form.skillsHidden;
  skillsText = document.getElementsByClassName('keyword-text');

  if (project_name.length < 3){
    alert("some things are wrong!");
    e.preventDefault();
  }

  else{
    errProjectName.innerText = "";
  }
  //
  if (!category){
    errCategory.innerText = "* Bir kategori seçin";
    e.preventDefault();
  }

  else{
    errCategory.innerText = "";
  }
  //
	if (budget_min != "" && budget_max != ""){

		if(budget_min < 10){
			errorBudget_min.innerText = "* En dusuk proje butçesi 10 TL olmalı";
	    e.preventDefault();
		}
		else{
	    errorBudget_min.innerText = "";
	  }
		if (budget_max > 100000){
	    errorBudget_max.innerText = "* En buyuk proje butçesini 100 bin TL olmalı";
	    e.preventDefault();
	  }

	  else{
	    errorBudget_max.innerText = "";
	  }
		if (budget_min >= budget_max){
	    errorBudget_max.innerText = "* Minimum değer maximumdan buyuk olamaz";
	    e.preventDefault();
	  }

	  else{
	    errorBudget_max.innerText = "";
	  }
	}

	if (description.length < 30){
		errorDescription.innerText = "* Açıklama en az 30 karakter içermeli";
		e.preventDefault()
	}
	else{
		errorDescription.innerText = "";
	}

  skills.value = "";

  if(skillsText.length > 5){
    errSkills.innerText = "* En fazla 5 yetenek yazmalısın"
    e.preventDefault();
  }

  if(skillsText.length == 0){
    errSkills.innerText = "* En az bir yetenek yazmalısın";
    e.preventDefault();
  }

  if(skillsText.length > 0 && skillsText.length < 6){
    errSkills.innerText = "";
  }


  for (item of skillsText){
    skills.value += item.innerText + "*";
  }

  return true;
}
