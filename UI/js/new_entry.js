
document.getElementById('postExams').addEventListener('submit', postExams);

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

    function postExams(event){
            event.preventDefault();

            token = window.localStorage.getItem('token');

            let admission_no = document.getElementById('admission_no').value;
            let term = document.getElementById('term').value;
            let form = document.getElementById('form').value;
            let type = document.getElementById('type').value;
            let maths = document.getElementById('maths').value;
            let english = document.getElementById('english').value;
            let kiswahili = document.getElementById('kiswahili').value;
            let chemistry = document.getElementById('chemistry').value;
            let biology = document.getElementById('biology').value;
            let physics = document.getElementById('physics').value;
            let history = document.getElementById('history').value;
            let geography = document.getElementById('geography').value;
            let cre = document.getElementById('cre').value;
            let agriculture = document.getElementById('agriculture').value;
            let business = document.getElementById('business').value;

            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/exams', {
                method: 'POST',
                headers : {
                Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
                body:JSON.stringify({admission_no:admission_no, term:term, form:form, type:type, maths:maths, english:english, kiswahili:kiswahili, chemistry:chemistry, biology:biology, physics:physics, history:history, geography:geography, cre:cre, agriculture:agriculture, business:business})
            }).then((res) => res.json())
            .then((data) =>  {

                console.log(data);
                let status = data['status'];
                let message = data['message'];
                if (status === '201'){
                    onSuccess('Exam entry successful');
                }else{
                    raiseError(message);
                }

            })
            .catch((err)=>{
                raiseError("Please check your internet connection and try again!");
                console.log(err);
            })
        }
