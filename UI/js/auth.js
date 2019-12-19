document.getElementById('postLogin').addEventListener('submit', postLogin);
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
    function postLogin(event){
            event.preventDefault();
            let email = document.getElementById('email').value;
            let password = document.getElementById('password').value;
            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/auth/login', {
                method: 'POST',
                headers : {
                Accept: 'application/json',
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify({email:email, password:password})
            }).then((res) => res.json())
            .then((data) =>  {
                console.log(data);
                let user = data['user'];
                let status = data['status'];
                let message = data['message'];
                if (status === '200'){
                    if (user.role === 'admin'){
                        localStorage.setItem('token', data.token);
                        localStorage.setItem('user', data.user);
                        localStorage.setItem('admission_no', data.user.admission_no);
                        localStorage.setItem('email', data.user.email);
                        onSuccess('Signed in successfully!');
                        window.location.replace('admin.html');
                    }
                    else if (user.role === 'bursar') {
                        localStorage.setItem('user', data.user);
                        localStorage.setItem('token', data.token);
                        localStorage.setItem('admission_no', data.user.admission_no);
                        localStorage.setItem('email', data.user.email);
                        onSuccess('Signed in successfully!');
                        window.location.replace('bursar.html');
                    }
                    else {
                        localStorage.setItem('user', data.user);
                        localStorage.setItem('token', data.token);
                        localStorage.setItem('admission_no', data.user.admission_no);
                        localStorage.setItem('email', data.user.email);
                        onSuccess('Signed in successfully!');
                        window.location.replace('user.html');
                    }
                }else{
                    raiseError(message);
                }
            })
            .catch((err)=> {
                raiseError("Please check your internet connection!");
                console.log(err);
            })
        }
