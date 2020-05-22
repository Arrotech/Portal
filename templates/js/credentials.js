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
admission = window.localStorage.getItem('admission_no');

fetch('https://njc-school-portal.herokuapp.com/api/v1/auth/users/' + admission, {
    method: 'GET',
    path: admission,
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
        console.log(data);
        if (status === "200") {
            var temp = "";

            temp += "<tr>" + "<th>Registration No.</th>" + " " + "<td>" + user.admission_no + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Surname</th>" + " " + "<td>" + user.surname + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Firstname</th>" + " " + "<td>" + user.firstname + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Lastname</th>" + " " + "<td>" + user.lastname + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Year</th>" + " " + "<td>" + user.current_year + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Gender</th>" + " " + "<td>" + user.gender + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Course</th>" + " " + "<td>" + user.stream + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Role</th>" + " " + "<td>" + user.role + "</td>" + "</tr>";
            temp += "<tr>" + "<th>Email</th>" + " " + "<td>" + user.email + "</td>" + "</tr>";

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




