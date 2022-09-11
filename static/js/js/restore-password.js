const loginPopup = document.getElementById("popup-login")
const forgotPasswordBtn = document.getElementById("forgot-password")


function SendEmail(){
    const email = document.getElementById("id_email").value
    if (email){
        document.location.href = '/account/reset-password?email=' + email
    }
}

document.getElementsByClassName("btn btn--accent js-popup")[0].onclick = () => {
    document.getElementById("login-popup-btn-div").innerHTML = '<button class="btn btn--accent" type="submit">Sign In</button>'
    loginPopup.getElementsByTagName("h3")[0].innerText = 'Login'
    document.getElementById("form-password").style.display = 'block'
    document.getElementById("popup-remember-me").style.display = 'flex'
}

forgotPasswordBtn.onclick = () => {
    document.getElementById("form-password").style.display = 'none'
    document.getElementById("popup-remember-me").style.display = 'none'
    document.getElementById("login-popup-btn-div").innerHTML = '<div class="btn btn--accent" onclick="SendEmail()">send code to email</div>'
    loginPopup.getElementsByTagName("h3")[0].innerText = "Forgot Password"

}

if (document.getElementById("close-message")){
    document.getElementById("close-message").onclick = () => {
        document.getElementsByClassName("error-toast")[0].style.display = 'none'
    }
}
