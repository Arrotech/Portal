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

    document.getElementById('getSubjects').onclick = () => {
            event.preventDefault();

            token = window.localStorage.getItem('token');
            admission = window.localStorage.getItem('admission_no');

            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/subjects/' + admission ,{
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
                    let status = data['status'];
                    let message = data['message'];
                        output = `
                            <div>
                                <table>
                                    <tr>
                                        <th>Subjects</th>
                                        <th>Marks</th>
                                    </tr>
                                    <tr>

                                        <td>Mathematics</td>
                                        <td>${data.subject.maths}</td>
                                    </tr>
                                    <tr>
                                        <td>English</td>
                                        <td>${data.subject.english}</td>
                                    </tr>
                                    <tr>
                                        <td>Kiswahili</td>
                                        <td>${data.subject.kiswahili}</td>
                                    </tr>
                                    <tr>
                                        <td>Chemistry</td>
                                        <td>${data.subject.chemistry}</td>
                                    </tr>
                                    <tr>
                                        <td>Biology</td>
                                        <td>${data.subject.biology}</td>
                                    </tr>
                                    <tr>
                                        <td>Physics</td>
                                        <td>${data.subject.physics}</td>
                                    </tr>
                                    <tr>
                                        <td>History</td>
                                        <td>${data.subject.history}</td>
                                    </tr>
                                    <tr>
                                        <td>Geography</td>
                                        <td>${data.subject.geography}</td>
                                    </tr>
                                    <tr>
                                        <td>Cre</td>
                                        <td>${data.subject.cre}</td>
                                    </tr>
                                    <tr>
                                        <td>Agriculture</td>
                                        <td>${data.subject.agriculture}</td>
                                    </tr>
                                    <tr>
                                        <td>Business</td>
                                        <td>${data.subject.business}</td>
                                    </tr>
                                </table>
                            </div>
                        `;
                    if (status === '200'){
                        document.getElementById('output').innerHTML = output;
                    }else{
                        raiseError(message);
                    }
                    })
            .catch((err)=>{
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
    }
