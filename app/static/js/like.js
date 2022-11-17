"use strict"
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

//Меню бургер

const iconMenu = document.querySelector('.menu__icon');
const menuBody = document.querySelector('.menu__body');
if (iconMenu){   
    iconMenu.addEventListener("click", function(e){
        document.body.classList.toggle('_lock');
        iconMenu.classList.toggle('_active');
        menuBody.classList.toggle('_active');
    });
}


// Прокрутка при клике

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

// /////////////////////////////////////////
console.log(123)
// function like_color() {
//   document.querySelector(".like_color").classList.toggle('image_like_red');
// }

let like_buttons = document.querySelectorAll(".like_color");
console.log(like_buttons)

for (let element of like_buttons){
  element.addEventListener("click", function() {
    element.classList.toggle('image_like_red');
  })
}

// ///////////////////////////////////////////


// $('.brise-upload > label').find('input').change(function() {
//   var file = this.files;
// $('.brise-upload > label').text('Selected file: ' + file[0].name);
// })

///////////////////////////////////////////////////////////////

// let comments = [];
// // loadComments();

// document.getElementById('comment-add').onclick = function(){
//     event.preventDefault();
//     let commentName = document.getElementById('comment-name');  // получили элементы формы
//     let commentBody = document.getElementById('comment-body');  // получили элементы формы

//     let comment = {
//         name : commentName.value, //получили имя того, кто написал комментарий
//         body : commentBody.value, // получили комментарий
//         time : Math.floor(Date.now() / 1000) // получили время комментария
//     }

//     commentName.value = ''; //очистили форму элемента
//     commentBody.value = ''; //очистили форму

//     comments.push(comment); // добавляем в массив наш массив на 121 строке
//     showComments();// выводим на экран
// }



// function showComments (){
//     let commentField = document.getElementById('comment-field');
//     let out = '';
//     comments.forEach(function(item){
//         // out += `<p class="text-right small"><em>${timeConverter(item.time)}</em></p>`;//время
//         // out += `<p class="alert alert-primary" role="alert">${item.name}</p>`;//имя
//         out += `<p class="alert alert-success" >${item.body}</p>`;//комментарий
//     });
//     commentField.innerHTML = out;
// }

// //конвертируем время
// function timeConverter(UNIX_timestamp){
//     var a = new Date(UNIX_timestamp * 1000);
//     var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
//     var year = a.getFullYear();
//     var month = months[a.getMonth()];
//     var date = a.getDate();
//     var hour = a.getHours();
//     var min = a.getMinutes();
//     var sec = a.getSeconds();
//     var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
//     return time;
//   }
//   console.log(comments)
///////////////////////////////////////////////////

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

console.log(toggleTheme)
console.log(123)
////////////////////////////////