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
const delete_post_url = "/delete_post"
let delete_post_request = new asyncRequest()

function remove_post_by_id(post_id) {
    let post = document.querySelector(`[post_id="${post_id}"]`)
    post.remove()
}

function delete_post(post_id) {
    let params = `post_id=${post_id}`
    delete_post_request.open("POST", delete_post_url, true)
    delete_post_request.send(params)
    delete_post_request.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                if (this.responseText != "0") {
                    remove_post_by_id(post_id)
                }
            }
        }
    }
    console.log(params)
}