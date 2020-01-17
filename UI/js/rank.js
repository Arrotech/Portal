function callToast() {

  var x = document.getElementById("snackbar");
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function onSuccess(msg){

    document.getElementById('snackbar').innerText = msg
    callToast();
}

function raiseError(msg){

    document.getElementById('snackbar').innerText = msg
    callToast();
}

document.getElementById('mybtn').onclick = () => {
        event.preventDefault();

        token = window.localStorage.getItem('token');
        admission = window.localStorage.getItem('admission_no');

        fetch('http://localhost:5000/api/v1/exams/' + admission, {
            method: 'GET',
            path: admission,
            headers : {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
        })
        .then((res) => res.json())
        .then((data) => {
          data.Exam.forEach(exam => {
                let status = data['status'];
                let message = data['message'];
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
                console.log(message);
                console.log(exam.maths);
                const total = math + eng + kis + chem + bio + phyc + hist + geo + c + agric + bus;
                const average = total/11;
                if (average >= 80 && average <= 100){
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

                const { admission_no, term, form, type, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business } = exam;
                rank += `
                    <div>
                        <table>
                            <tr>
                                <th>Admission No.</th>
                                <th>Term</th>
                                <th>Form</th>
                                <th>Type</th>
                                <th>Mathematics</th>
                                <th>English</th>
                                <th>Kiswahili</th>
                                <th>Chemistry</th>
                                <th>Biology</th>
                                <th>Physics</th>
                                <th>History</th>
                                <th>Geography</th>
                                <th>Cre</th>
                                <th>Agriculture</th>
                                <th>Business</th>
                                <th>Total</th>
                                <th>Average</th>
                                <th>Grade</th>
                                <th>Points</th>
                            </tr>
                            <tr>
                                <td>${exam.admission_no}</td>
                                <td>${exam.term}</td>
                                <td>${exam.form}</td>
                                <td>${exam.type}</td>
                                <td>${exam.maths}</td>
                                <td>${exam.english}</td>
                                <td>${exam.kiswahili}</td>
                                <td>${exam.chemistry}</td>
                                <td>${exam.biology}</td>
                                <td>${exam.physics}</td>
                                <td>${exam.history}</td>
                                <td>${exam.geography}</td>
                                <td>${exam.cre}</td>
                                <td>${exam.agriculture}</td>
                                <td>${exam.business}</td>
                                <td>${total}</td>
                                <td>${average}</td>
                                <td>${grade}</td>
                                <td>${points}</td>
                            </tr>
                        </table>
                    </div>
                `;
                if (status === '200'){
                    document.getElementById('rank').innerHTML = rank;
                }
                else{
                    console.log(message);
                    raiseError(message);
                }
                });
                })
        .catch((err)=>{
            raiseError("Please check your internet connection and try again!");
            console.log(err);
        })
}
