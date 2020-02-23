function viewConfirmPassword() {
    var x = document.getElementById("confirm_password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }