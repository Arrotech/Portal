function logout() {
    event.preventDefault();
    window.localStorage.clear()
    window.location.replace('accountant_login.html')
}