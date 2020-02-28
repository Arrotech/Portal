function logout() {
    event.preventDefault();
    window.localStorage.clear()
    window.location.replace('staff_login.html')
}