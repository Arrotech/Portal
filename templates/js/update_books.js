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

            let book_id = document.getElementById('book_id').value;
            let admission_no = document.getElementById('admission_no').value;
            let book_no = document.getElementById('book_no').value;
            let author = document.getElementById('author').value;
            let title = document.getElementById('title').value;
            let subject = document.getElementById('subject').value;
            let form = document.getElementById('form').value;
            let stream = document.getElementById('stream').value;


            fetch('https://njc-school-portal.herokuapp.com/api/v1/books/' + book_id, {
                method: 'PUT',
                path: book_id,
                headers : {
                Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
                body:JSON.stringify({admission_no:admission_no, book_no:book_no, author:author, title:title, subject:subject, form:form, stream:stream})
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
