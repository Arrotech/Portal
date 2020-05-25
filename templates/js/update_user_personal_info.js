document.getElementById('updateUserPersonalInfo').addEventListener('submit', updateUserPersonalInfo);

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

    function updateUserPersonalInfo(event){
            event.preventDefault();

            token = window.localStorage.getItem('token');
            user_id = window.localStorage.getItem('user_id');
            admission = window.localStorage.getItem('admission_no');

            let firstname = document.getElementById('firstname').value;
            let lastname = document.getElementById('lastname').value;
            let surname = document.getElementById('surname').value;


            fetch('https://njc-school-portal.herokuapp.com/api/v1/auth/users/user_info/' + admission, {
                method: 'PUT',
                path: admission,
                headers : {
                Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
                body:JSON.stringify({firstname:firstname, lastname:lastname, surname:surname})
            }).then((res) => res.json())
            .then((data) =>  {

                console.log(data);
                let status = data['status'];
                let message = data['message'];
                if (status === '200'){
                    onSuccess(message);
                }else{
                    raiseError(message);
                }

            })
            .catch((err)=>{
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
        }
