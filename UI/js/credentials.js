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

            temp += "<tr>";
            temp += "<td>" + user.admission_no + "</td>";
            temp += "<td>" + user.surname + " " + user.firstname + " " + user.lastname +"</td>";
            temp += "<td>" + user.email + "</td></tr>";

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




