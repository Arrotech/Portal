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


token = window.localStorage.getItem('token');
user = window.localStorage.getItem('user');
uname = window.localStorage.getItem('username');

fetch('https://njc-school-portal.herokuapp.com/api/v1/auth/staff/users/' + uname, {
    method: 'GET',
    path: uname,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    },
})
    .then((res) => res.json())
    .then((data) => {
        let status = data['status'];
        let message = data['message'];
        let user = data.user;
        console.log(data.user);
        if (status === "200") {
            var temp = "";

            temp += "<tr>" + "<th>Username</th>" + " " + "<td>" + user.username + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Firstname</th>" + " " + "<td>" + user.firstname + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Lastname</th>" + " " + "<td>" + user.lastname + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Form</th>" + " " + "<td>" + user.form + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Stream</th>" + " " + "<td>" + user.stream + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Role</th>" + " " + "<td>" + user.role + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Email</th>" + " " + "<td>" + user.email + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Date created</th>" + " " + "<td>" + user.date + "</td>" + "</tr>";

            document.getElementById("data").innerHTML = temp;
        }
        else {
            raiseError(message);
        }

    })
    .catch((err) => {
        raiseError("Please check your internet connection and try again!");
        console.log(err);
    })




