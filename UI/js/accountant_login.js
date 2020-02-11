document.getElementById('accountantLogin').addEventListener('submit', accountantLogin);
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
    function accountantLogin(event){
            event.preventDefault();
            let email = document.getElementById('email').value;
            let password = document.getElementById('password').value;
            fetch('https://njc-school-portal.herokuapp.com/api/v1/auth/accountant/login', {
                method: 'POST',
                headers : {
                Accept: 'application/json',
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify({email:email, password:password})
            }).then((res) => res.json())
            .then((data) =>  {
                console.log(data);
                let status = data['status'];
                let message = data['message'];
                if (status === '200'){
                    localStorage.setItem('user', data.user);
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('username', data.user.username);
                    localStorage.setItem('email', data.user.email);
                    onSuccess('Signed in successfully!');
                    window.location.replace('bursar.html');
                }else{
                    raiseError(message);
                }
            })
            .catch((err)=> {
                raiseError("Please check your internet connection!");
                console.log(err);
            })
        }
