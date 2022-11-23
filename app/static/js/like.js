"use strict"

function asyncRequest(){
    try{
        var request = new XMLHttpRequest()
    }
    catch(e1){
        try{
            request = new ActiveXObject("XMLHTTP")
        }
        catch(e2){
            try{
            request = new ActiveXObject("Microsoft.XMLHTTP")
            }
            catch(e3){
                request = false
            }
        }
    }
    return request
}

let heart = document.querySelectorAll('.heart');
let likesNumber = document.querySelectorAll('.likes-number');
const like_loader_url = "/like_loader"
let like_request = new asyncRequest()

for (let element of heart){
  element.addEventListener("click", function() {

    const post_id = element.getAttribute('post_id')
    let params = `post_id=${post_id}`
    like_request.open("POST", like_loader_url, true)
    like_request.send(params)
    console.log(params)
    like_request.onreadystatechange = function(){
        if (this.readyState == 4){
            if (this.status == 200){
                if (this.responseText != null){
                    if (element.classList.contains('added')){
                        element.querySelector('span').innerText = parseInt(element.querySelector('span').innerText) - 1
                    } else{
                        element.querySelector('span').innerText = parseInt(element.querySelector('span').innerText) + 1
                    }
                }
            }
        }
    }
    element.classList.toggle('added');
  })
}

const isMobile = {
    Android: function(){
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function(){
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function(){
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function(){
        return navigator.userAgent.match(/Opera mini/i);
    },
    Windows: function(){
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function(){
        return(
            isMobile.Android()||
            isMobile.BlackBerry()||
            isMobile.iOS()||
            isMobile.Opera()||
            isMobile.Windows()
        );
    }
};

if (isMobile.any()){
    document.body.classList.add('_touch');

    let menuArrows = document.querySelectorAll('.menu__arrow');
    if (menuArrows.length > 0){
        for (let index = 0; index < menuArrows.length; index++) {
            const menuArrow = menuArrows[index];
            menuArrow.addEventListener("click", function(e){
                menuArrow.parentElement.classList.toggle('_active');
            });
            
        }
    }

} else{
    document.body.classList.add('_pc');
}

const iconMenu = document.querySelector('.menu__icon');
const menuBody = document.querySelector('.menu__body');
if (iconMenu){   
    iconMenu.addEventListener("click", function(e){
        document.body.classList.toggle('_lock');
        iconMenu.classList.toggle('_active');
        menuBody.classList.toggle('_active');
    });
}

const menuLinks = document.querySelectorAll('.menu__link[data-goto]');
if (menuLinks.length > 0){
    menuLinks.forEach(menuLink => {
        menuLink.addEventListener("click", onMenuLinkClick);
    });

    function onMenuLinkClick(e){
        const menuLink = e.target;
        if (menuLink.dataset.goto && document.querySelector(menuLink.dataset.goto)){
            const gotoBlock = document.querySelector(menuLink.dataset.goto);
            const gotoBlockValue = gotoBlock.getBoundingClientRect().top + pageYOffset - document.querySelector('header').offsetHeight;
        
            if (iconMenu.classList.contains('_active')){
                document.body.classList.remove('_lock');
                iconMenu.classList.remove('_active');
                menuBody.classList.remove('_active');
            }

            window.scrollTo({
                top:gotoBlockValue,
                behavior:"smooth"
            });
            e.preventDefault();
        }
    }
}

function theme() {
  const toggleTheme = document.querySelector('.toggle-theme')
  let el = document.documentElement

  toggleTheme.addEventListener('click', () =>{
    if (el.hasAttribute('data-theme')){
      el.removeAttribute('data-theme')
      localStorage.removeItem('theme')
    }
    else{
      el.setAttribute('data-theme', 'dark')
      localStorage.setItem('theme', 'dark')
    }
  })

  if (localStorage.getItem('theme')){
    el.setAttribute('data-theme', 'dark')
  }
}

theme()

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





{/* <form action="{{url_for('login')}}" method="post" class="login_form">
<div class="line">
  <label for="username">Имя:</label>
  <input type="text" name="username" id="username">
</div>
<div class="line">
  <label for="pwd">Пароль:</label>
  <input type="text" name='pwd', id='pwd'>
</div>
<div class="wrap-line">
  <div class="brise-input">
    <label for="save_me">Запомнить меня</label>
    <input type="radio" name="rb_me">
    <span class="line"></span>
  </div>
</div>
<input type="submit" value="Создать">
</form> */}
