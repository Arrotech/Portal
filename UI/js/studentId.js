document.getElementById('getId').addEventListener('click', getId);

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

    function getId(event){
            event.preventDefault();

            token = window.localStorage.getItem('token');

            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/id' ,{
                method: 'GET',
                headers : {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
            })
            .then((res) => res.json())
            .then((data) => {
                let output = `<h3 style="margin-left: 10px;"> Books grouped by Admission Number.</h3>`;
                data.students.forEach(student => {
                    let status = data['status'];
                    let message = data['message'];
                    const { student_id, surname, first_name, last_name, admission_no } = student;
                    output += `
                        <div>
                            <h4 style="margin-left: 10px; text-decoration:none; color: #d65050;">Registration No: ${student.admission_no}</h4>
                            <h4 style="margin-left: 10px; text-decoration:none; color: #d65050;">Exam ID: ${student.student_id}</h4>

                            <p>Fullname: ${student.first_name} ${student.last_name}</p>
                            <p>Surname: ${student.surname}</p>
                            <p>Admission: ${student.admission_no}</p>
                        </div>
                    `;
                    if (status === '200'){
                        document.getElementById('output').innerHTML = output;
                    }else{
                        raiseError(message);
                    }
                    });
                    })
            .catch((err)=>{
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
    }
