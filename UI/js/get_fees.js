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

document.getElementById('getFees').onclick = () => {
        event.preventDefault();

        token = window.localStorage.getItem('token');
        admission = window.localStorage.getItem('admission_no');

        fetch('https://arrotech-school-portal.herokuapp.com/api/v1/fees/' + admission ,{
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
            data.Fee.forEach(fee => {
                let status = data['status'];
                let message = data['message'];
                const { admission_no, transaction_type, transaction_no, description, amount } = fee;
                output += `
                    <div>
                        <table>
                            <tr>
                                <th>Transaction type</th>
                                <th>Transaction No.</th>
                                <th>Description</th>
                                <th>Amount</th>
                            </tr>
                            <tr>
                                <td>${fee.transaction_type}</td>
                                <td>${fee.transaction_no}</td>
                                <td>${fee.description}</td>
                                <td>${fee.amount}</td>
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
