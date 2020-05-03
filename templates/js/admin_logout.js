function logout() {
    onclick = (event) => {
        event.preventDefault();
        window.localStorage.clear();
        window.location.replace('staff_login.html');
    }
}