
let password = document.querySelector('.password');
let securityBar = document.querySelector('.security-bar');
let showPassword = document.querySelector('.show-password');
console.log(password)
console.log(showPassword)
console.log(123)

showPassword.onchange = function () {
  if (showPassword.checked) {
    password.type = 'text';
  } else {
    password.type = 'password';
  }
};


password.oninput = function () {
  let passLength = password.value.length;
  securityBar.style.width = passLength * 10 + '%';
  if (passLength <= 5) {
    securityBar.style.backgroundColor = 'red';
  } else if (passLength > 5 && passLength < 10) {
    securityBar.style.backgroundColor = 'gold';
  } else {
    securityBar.style.backgroundColor = 'green';
  }

};