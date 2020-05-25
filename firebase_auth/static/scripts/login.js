(function() {
   
    const txtEmail = document.getElementById('txtEmail');
    const txtPassWord = document.getElementById('txtPassword');
    const btnLogin = document.getElementById('btnLogin');
    const csrfToken = document.getElementById('csrf_token');
    const btnLogOut = document.getElementById('btnLogOut')
    const btnGoogle = document.getElementById('btnGoogle')
    const btnFacebook = document.getElementById('btnFacebook')
    /*function postIdTokenToSessionLogin(endPoint, idToken, csrfToken) {
        const xhttp = new XMLHttpRequest;
        let jsonData = {idToken: idToken}
        xhttp.open("POST", endPoint, idToken);
        xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("X-CSRFToken", csrfToken); // CSRF Protection
        xhttp.send(JSON.stringify(jsonData));
    };*/
    const postIdTokenToSessionLogin = (url, idToken, csrfToken) => {
        // POST to session login endpoint.
        return $.ajax({
          type:'POST',
          headers: {
            'X-CSRFToken': csrfToken
          },
          url: url,
          data: {idToken: idToken},
          dataType: 'json',
          contentType: 'application/x-www-form-urlencoded'
        });
      };


    // Add Email/Password Login Event
    btnLogin.addEventListener('click', e => {
        // Get Email and Pass
        const email = txtEmail.value;
        const pass = txtPassword.value;
        const auth = firebase.auth();

        // As httpOnly cookies are to be used, do not persist any state client side.
        auth.setPersistence(firebase.auth.Auth.Persistence.NONE);
        
        // Sign In
        auth.signInWithEmailAndPassword(email, pass).then(({ user }) => {
            // Get the user's ID token as it is needed to exchange for a session cookie.
            return user.getIdToken().then(idToken => {
                // Session login endpoint is queried and the session cookie is set.
                return postIdTokenToSessionLogin('/sessionLogin', idToken, csrfToken.value);
            });
        }).then(() => {
            // A page redirect would suffice as the persistence is set to NONE.
            return auth.signOut();
        }).then(() => {
            window.location.assign('/profile');
        });
    });

    // Add Oauth2 Sign In With Google Login Event
    btnGoogle.addEventListener('click', e=> {
        const auth = firebase.auth();
        const provider = new firebase.auth.GoogleAuthProvider();

        // As httpOnly cookies are to be used, do not persist any state client side.
        auth.setPersistence(firebase.auth.Auth.Persistence.NONE);

         // Sign In
         auth.signInWithPopup(provider).then(({ user }) => {
            // Get the user's ID token as it is needed to exchange for a session cookie.
            return user.getIdToken().then(idToken => {
                // Session login endpoint is queried and the session cookie is set.
                return postIdTokenToSessionLogin('/sessionLogin', idToken, csrfToken.value);
            });
        }).then(() => {
            // A page redirect would suffice as the persistence is set to NONE.
            return auth.signOut();
        }).then(() => {
            window.location.assign('/profile');
        });
    });

    // Add Oauth2 Sign In With Facebook Login Event
    btnFacebook.addEventListener('click', e=> {
        const auth = firebase.auth();
        const provider = new firebase.auth.FacebookAuthProvider();

        // As httpOnly cookies are to be used, do not persist any state client side.
        auth.setPersistence(firebase.auth.Auth.Persistence.NONE);

         // Sign In
         auth.signInWithPopup(provider).then(({ user }) => {
            // Get the user's ID token as it is needed to exchange for a session cookie.
            return user.getIdToken().then(idToken => {
                // Session login endpoint is queried and the session cookie is set.
                return postIdTokenToSessionLogin('/sessionLogin', idToken, csrfToken.value);
            });
        }).then(() => {
            // A page redirect would suffice as the persistence is set to NONE.
            return auth.signOut();
        }).then(() => {
            window.location.assign('/profile');
        });
    });

        
    
}());

