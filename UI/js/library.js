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

    document.getElementById('getBooks').onclick = () => {
            event.preventDefault();

            token = window.localStorage.getItem('token');
            admission = window.localStorage.getItem('admission_no');

            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/books/' + admission ,{
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
                data.Book.forEach(book => {
                    let status = data['status'];
                    let message = data['message'];
                    const { admission_no, book_no, author, title, subject } = book;
                    output += `
                        <div>
                            <table>
                                <tr>
                                    <th>Book No.</th>
                                    <th>Author</th>
                                    <th>Title</th>
                                    <th>Subject</th>
                                </tr>
                                <tr>
                                    <td>${book.book_no}</td>
                                    <td>${book.author}</td>
                                    <td>${book.title}</td>
                                    <td>${book.subject}</td>
                                </tr>
                            </table>
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
