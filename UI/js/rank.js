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

fetch('https://njc-school-portal.herokuapp.com/api/v1/exams/' + admission, {
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
    if (status === "200") {
      var temp = "";
      data.Exam.forEach((exam) => {
        let math = Number(exam.maths);
        let eng = Number(exam.english);
        let kis = Number(exam.kiswahili);
        let chem = Number(exam.chemistry);
        let bio = Number(exam.biology);
        let phyc = Number(exam.physics);
        let hist = Number(exam.history);
        let geo = Number(exam.geography);
        let c = Number(exam.cre);
        let agric = Number(exam.agriculture);
        let bus = Number(exam.business);
        const total = math + eng + kis + chem + bio + phyc + hist + geo + c + agric + bus;
        const average = total / 11;
        if (average >= 80 && average <= 100) {
          grade = 'A';
          points = '12';
        }
        else if (average >= 75 && average < 80) {
          grade = 'A-';
          points = '11';
        }
        else if (average >= 70 && average < 75) {
          grade = 'B+';
          points = '10';
        }
        else if (average >= 65 && average < 70) {
          grade = 'B';
          points = '9';
        }
        else if (average >= 60 && average < 65) {
          grade = 'B-';
          points = '8';
        }
        else if (average >= 55 && average < 60) {
          grade = 'C+';
          points = '7';
        }
        else if (average >= 50 && average < 55) {
          grade = 'C';
          points = '6';
        }
        else if (average >= 45 && average < 50) {
          grade = 'C-';
          points = '5';
        }
        else if (average >= 40 && average < 45) {
          grade = 'D+';
          points = '4';
        }
        else if (average >= 35 && average < 40) {
          grade = 'D';
          points = '3';
        }
        else if (average >= 30 && average < 35) {
          grade = 'D-';
          points = '2';
        }
        else if (average >= 0 && average < 30) {
          grade = 'E';
          points = '1';
        }

        temp += "<tr>";
        temp += "<td>" + exam.term + "</td>";
        temp += "<td>" + exam.form + "</td>";
        temp += "<td>" + exam.type + "</td>";
        temp += "<td>" + exam.maths + "</td>";
        temp += "<td>" + exam.english + "</td>";
        temp += "<td>" + exam.kiswahili + "</td>";
        temp += "<td>" + exam.chemistry + "</td>";
        temp += "<td>" + exam.biology + "</td>";
        temp += "<td>" + exam.physics + "</td>";
        temp += "<td>" + exam.history + "</td>";
        temp += "<td>" + exam.geography + "</td>";
        temp += "<td>" + exam.cre + "</td>";
        temp += "<td>" + exam.agriculture + "</td>";
        temp += "<td>" + exam.business + "</td>";
        temp += "<td>" + total + "</td>";
        temp += "<td>" + average + "</td>";
        temp += "<td>" + grade + "</td>";
        temp += "<td>" + points + "</td></tr>";

      })
      document.getElementById("data").innerHTML = temp;
    }
    else {
      raiseError(message);
    }

  })
  .catch((err) => {
    raiseError("Please check your internet connection and try again!");
  })

