"use strict"

function asyncRequest() {
    try {
        var request = new XMLHttpRequest()
    } catch (e1) {
        try {
            request = new ActiveXObject("XMLHTTP")
        } catch (e2) {
            try {
                request = new ActiveXObject("Microsoft.XMLHTTP")
            } catch (e3) {
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
for (let element of heart) {
    element.addEventListener("click", function() {
        const post_id = element.getAttribute('post_id')
        let params = `post_id=${post_id}`
        like_request.open("POST", like_loader_url, true)
        like_request.send(params)
        console.log(params)
        like_request.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    if (this.responseText != null) {
                        element.querySelector('span').innerText = this.responseText
                    }
                }
            }
        }
        element.classList.toggle('added');
    })
}