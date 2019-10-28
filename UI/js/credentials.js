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

    document.getElementById('getId').onclick = () => {
            event.preventDefault();

            token = window.localStorage.getItem('token');
            admission = window.localStorage.getItem('admission_no');

            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/auth/users/' + admission, {
                method: 'GET',
                path: admission,
                headers : {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
            }).then((res) => res.json())
            .then((data) =>  {
                data.Users.forEach(user => {
                    let status = data['status'];
                    let message = data['message'];
                    console.log(status);
                    const { surname, firstname, lastname, admission_no, email, password, form, role  } = user;
                    output += `
                        <div>
                        <div>
                            <table>
                                <tr>
                                    <th>Admission No.</th>
                                    <th>Surname</th>
                                    <th>First Name</th>
                                    <th>Last Name</th>
                                </tr>
                                <tr>
                                    <td>${id.admission_no}</td>
                                    <td>${id.surname}</td>
                                    <td>${id.firstname}</td>
                                    <td>${id.lastname}</td>
                                </tr>
                            </table>
                        </div>
                        </div>
                    `;
                if (status === '200'){
                    widocument.getElementById('output').innerHTML = output;
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
