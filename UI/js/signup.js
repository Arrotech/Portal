
document.getElementById('postSignup').addEventListener('submit', postSignup);

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

function postSignup(event){
            event.preventDefault();

            let firstname = document.getElementById('firstname').value;
            let lastname = document.getElementById('lastname').value;
            let surname = document.getElementById('surname').value;
            let admission_no = document.getElementById('admission_no').value;
            let email = document.getElementById('email').value;
            let password = document.getElementById('password').value;
            let form = document.getElementById('form').value;

            fetch('https://njc-school-portal.herokuapp.com/api/v1/auth/register', {
                method: 'POST',
                headers : {
                    Accept: 'application/json',
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify({firstname:firstname, lastname:lastname, surname:surname, admission_no:admission_no, email:email, password:password, form:form})
            }).then((res) => res.json())
            .then((data) =>  {
                console.log(data);
                let status = data['status'];
                let message = data['message'];
                if (status === '201'){
                    localStorage.setItem("user", JSON.stringify(data[0]));
                    localStorage.setItem('user', data.user);
                    localStorage.setItem('admission_no', data.user.admission_no);
                    localStorage.setItem('email', data.user.email);
                    onSuccess('Account created successfully!');
                    window.location.replace('user.html');

                }else{
                    raiseError(message);
                }
            })
            .catch((err)=>{
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
        }
