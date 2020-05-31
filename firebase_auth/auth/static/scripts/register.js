(function() {
    const txtName = document.getElementById('txtName');
    const txtEmail = document.getElementById('txtEmail');
    const txtPassword = document.getElementById('txtPassword')
    const txtConfirmPassword = document.getElementById('txtConfirmPassword')
    const btnSubmit = document.getElementById('btnSubmit')


    // Register User on submit
    const auth = firebase.auth()
    const email = txtEmail.value
    const pass = txtPassword.value
    const confirmPass = txtConfirmPassword.value

    // Confirm Password
    if (pass === confirmPass) {
        auth.createUserWithEmailAndPassword(email, pass).then(user => {
            return user.sendEmailVerification().then(() => {
                // Post to register endpoint on server for rest of information
            }).catch(error => {
                console.log(error);
            });
        }).catch(error => {
            const errorCode = error.code;
            const errorMessage = error.message;
            console.log(errorCode, errorMessage);
        });
    } else {
        // Notify User PW's don't match
    };
}());