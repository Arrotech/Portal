function logout() {
    event.preventDefault();
    window.localStorage.clear()
    window.location.replace('login.html')
}