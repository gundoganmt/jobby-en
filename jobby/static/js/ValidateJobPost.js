var form = document.getElementById('post_job');

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
  form.addEventListener('submit', (e) =>{
    c = document.getElementsByClassName("closeable");
    for (let item of c){
      item.style.display='none';
    }

    var job_name = form.job_name.value;
    var job_type = form.job_type.value;
    var category = form.category.value;
    var location = form.location.value;
    var salary_min = parseInt(form.salary_min.value);
    var salary_max = parseInt(form.salary_max.value);
    var exp_min = parseInt(form.exp_min.value);
    var exp_max = parseInt(form.exp_max.value);
    var quill = document.querySelector('#quillField');
    var editor = document.querySelector('#editor');
    quill.value = editor.children[0].innerHTML;


    if (job_name.length < 5){
      createErrField("İlan başlığı çok kısa!");
      e.preventDefault();
    }
    if (!job_type){
      createErrField("Lütfen iş tipini seçiniz!");
      e.preventDefault();
    }
    if (!category){
      createErrField("Lütfen kategori seçiniz!");
      e.preventDefault();
    }
    if (!location){
      createErrField("Lütfen yeri seçin!");
      e.preventDefault();
    }
    if (salary_min > salary_max){
      createErrField("Düşük maaş, yüksek maaştan fazla olamaz!");
      e.preventDefault();
    }
    if (exp_min > exp_max){
      createErrField("En az tecrübe, en çok tecrübeden fazla olamaz!");
      e.preventDefault();
    }
    if (quill.length < 30){
      createErrField("Lütfen iş ilanınızı biraz açıklayın. En az 30 karakter.");
      e.preventDefault();
    }
  });
})
