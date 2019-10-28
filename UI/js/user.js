document.getElementById('userProfile').addEventListener('click', userProfile);

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

    function userProfile(event){
            event.preventDefault();

            token = window.localStorage.getItem('token');
            user_id = window.localStorage.getItem('user_id');


            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/users/' + user_id,{
                method: 'GET',
                path: user_id,
                headers : {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
            })
            .then((res) => res.json())
            .then((data) => {
                let output = `<h3 style="margin-left: 10px;"> User Information.</h3>`;
                data.users.forEach(user => {
                    const { user_id, firstname, surname, admission_no, email } = user
                    output += `
                        <div>
                            <h4 style="margin-left: 10px; text-decoration:none; color: #d65050;">Exam ID: ${user.user_id}</h4>
                            <table>
                                <tr>
                                    <th>Name</th>
                                    <th>Details</th>
                                </tr>
                                <tr>

                                    <td>Firstname</td>
                                    <td>${user.firstname}</td>
                                </tr>
                                <tr>
                                    <td>Surname</td>
                                    <td>${user.surname}</td>
                                </tr>
                                <tr>
                                    <td>Registration No</td>
                                    <td>${user.admission_no}</td>
                                </tr>
                                <tr>
                                    <td>Form</td>
                                    <td>${user.email}</td>
                                </tr>
                            </table>
                        </div>
                    `;
                            document.getElementById('output').innerHTML = output;
                        });
                    })
            .catch((err)=>{
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
    }
