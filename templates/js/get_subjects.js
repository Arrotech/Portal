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

fetch('https://njc-school-portal.herokuapp.com/api/v1/subjects/' + admission, {
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
        let sub = data.subject;

        if (status === "200") {
            var temp = "";

            temp += "<tr>";
            temp += "<td>" + sub.admission_no + "</td>";
            temp += "<td>" + sub.maths + "</td>";
            temp += "<td>" + sub.english + "</td>";
            temp += "<td>" + sub.kiswahili + "</td>";
            temp += "<td>" + sub.chemistry + "</td>";
            temp += "<td>" + sub.biology + "</td>";
            temp += "<td>" + sub.physics + "</td>";
            temp += "<td>" + sub.history + "</td>";
            temp += "<td>" + sub.geography + "</td>";
            temp += "<td>" + sub.cre + "</td>";
            temp += "<td>" + sub.agriculture + "</td>";
            temp += "<td>" + sub.business + "</td></tr>";

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
