var form = document.getElementById('register-account-form');
form.addEventListener('submit', validate);

function validate(e){

  var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  var name = form.name.value;
  var surname = form.surname.value;
  var email = form.email.value;
  var password = form.password.value;
  var confirm = form.confirm.value;
  var errName = document.getElementById('errorName');
  var errLastName = document.getElementById('errorLastName');
  var errPassword = document.getElementById('errorPassword');
  var errEmail = document.getElementById('errorEmail');
  var errConfirm = document.getElementById('errorConfirm');

  if (name.length < 3){
    errName.innerText = "isim çok kısa";
    e.preventDefault();
  }

  else{
    errName.innerText = "";
  }

  if (surname.length < 2){
    errLastName.innerText = "soy isim çok kısa";
    e.preventDefault();
  }

  else{
    errLastName.innerText = "";
  }

  if(!filter.test(email)){
    errEmail.innerText = "geçersiz email";
    e.preventDefault();
  }

  else{
    errEmail.innerText = "";
  }

  if (password.length < 6){
    errPassword.innerText = "şifre çok kısa";
    e.preventDefault();
  }

  else{
    errPassword.innerText = "";
  }

  if (confirm != password){
    errConfirm.innerText = "Parolalar uyuşmuyor";
    e.preventDefault();
  }

  else{
    errConfirm.innerText = "";
  }

  return true;
}
