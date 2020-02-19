
document.getElementById('staffSignup').addEventListener('submit', staffSignup);

function callToast() {

    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}

function onSuccess(msg) {

    document.getElementById('snackbar').innerText = msg
    callToast();
}

function raiseError(msg) {

    document.getElementById('snackbar').innerText = msg
    callToast();
}

function staffSignup(event) {
    event.preventDefault();
    var pswd = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    if (pswd != confirmPassword) {
        raiseError("Passwords do not match.");
    } else {
        let firstname = document.getElementById('firstname').value;
        let lastname = document.getElementById('lastname').value;
        let form = document.getElementById('form').value;
        let username = document.getElementById('username').value;
        let email = document.getElementById('email').value;
        let password = document.getElementById('password').value;

        fetch('https://njc-school-portal.herokuapp.com/api/v1/auth/staff/register', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ firstname: firstname, lastname: lastname, form: form, username: username, email: email, password: password })
        }).then((res) => res.json())
            .then((data) => {

                console.log(data);
                let user = data['user'];
                let status = data['status'];
                let message = data['message'];
                if (status === '201') {
                    localStorage.setItem("user", JSON.stringify(data[0]));
                    localStorage.setItem('user', data.user);
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('firstname', data.user.firstname);
                    localStorage.setItem('lastname', data.user.lastname);
                    localStorage.setItem('username', data.user.username);
                    localStorage.setItem('email', data.user.email);
                    onSuccess('Account created successfully!');
                    window.location.replace('admin.html');
                } else {
                    raiseError(message);
                }
            })
            .catch((err) => {
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
    }


}
