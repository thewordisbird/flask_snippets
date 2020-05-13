(function() {
    // As httpOnly cookies are to be used, do not persist any state client side.
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);

    // Get Elements
    const loginForm = document.getElementById('loginForm');
    const txtEmail = document.getElementById('txtEmail');
    const txtPassWord = document.getElementById('txtPassword');
    const btnLogin = document.getElementById('btnLogin');
    const btnSignOUt = document.getElementById('btnSignOut');
    const csrfToken = document.getElementById('csrf_token');
    //const userIdToken = document.getElementById('id_token');

    function postIdTokenToSessionLogin(endPoint, idToken, csrfToken) {
        const xhttp = new XMLHttpRequest;
        let jsonData = {idToken: idToken, csrfToken: csrfToken}
        xhttp.open("POST", endPoint, idToken, true);
        xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify(jsonData));
    };

    // Add Login Event
    loginForm.addEventListener('submit', e=> {
        // Prevent From Submit
        e.preventDefault()

        // Get Email and Pass
        const email = txtEmail.value;
        const pass = txtPassword.value;
        const auth = firebase.auth();
        
        // Sign In
        const promise = auth.signInWithEmailAndPassword(email, pass).then(({ user }) => {
            //console.log(user.getIdToken())
            //console.log(document.getElementById('csrf_token').value)

            
            // Get the user's ID token as it is needed to exchange for a session cookie.
            return user.getIdToken().then(idToken => {
                // Session login endpoint is queried and the session cookie is set.
                // CSRF protection should be taken into account.
                // ...
                //console.log(idToken);
                //const csrfToken = document.getElementById('csrf_token').value;
                //userIdToken.value = idToken;
                //loginForm.submit()
                return postIdTokenToSessionLogin('/sessionLogin', idToken, csrfToken.value);
            });
        }).then(() => {
                // A page redirect would suffice as the persistence is set to NONE.
                return firebase.auth().signOut();
            }).then(() => {
                window.location.assign('/profile');
            });
        });
        
    

    

    // Sign Out 
    btnSignOUt.addEventListener('click', e=> {
        firebase.auth().signOut();
    });

    // Add Realtime Status Listener
    firebase.auth().onAuthStateChanged(firebaseUser => {
        if (firebaseUser) {
            console.log('logged in');
            btnSignOUt.classList.remove('hide')
        } else {
            console.log('Not logged in');
            btnSignOUt.classList.add('hide')
        }
    });
}());