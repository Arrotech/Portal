document.getElementById('updateBooks').addEventListener('submit', updateBooks);

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

    function updateBooks(event){
            event.preventDefault();

            token = window.localStorage.getItem('token');


            let admission_no = document.getElementById('admission_no').value;
            let author = document.getElementById('author').value;
            let title = document.getElementById('title').value;
            let subject = document.getElementById('subject').value;


            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/books/' + admission_no, {
                method: 'PUT',
                path: admission_no,
                headers : {
                Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
                body:JSON.stringify({admission_no:admission_no, author:author, title:title, subject:subject})
            }).then((res) => res.json())
            .then((data) =>  {

                console.log(data);
                let status = data['status'];
                let message = data['message'];
                if (status === '200'){
                    onSuccess('Books updated successfully!');
                }else{
                    raiseError(message);
                }

            })
            .catch((err)=>{
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
        }
