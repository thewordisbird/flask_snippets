(function() {
   
    const loginForm = document.getElementById('loginForm');
    const txtEmail = document.getElementById('txtEmail');
    const txtPassWord = document.getElementById('txtPassword');
    const btnLogin = document.getElementById('btnLogin');
    const csrfToken = document.getElementById('csrf_token');
    const btnLogOut = document.getElementById('btnLogOut')

    /*function postIdTokenToSessionLogin(endPoint, idToken, csrfToken) {
        const xhttp = new XMLHttpRequest;
        let jsonData = {idToken: idToken}
        xhttp.open("POST", endPoint, idToken);
        xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("X-CSRFToken", csrfToken); // CSRF Protection
        xhttp.send(JSON.stringify(jsonData));
    };*/
    const postIdTokenToSessionLogin = function(url, idToken, csrfToken) {
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
        firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);
        
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
    function onSignIn(googleUser) {
        console.log('Google Auth Response', googleUser);
        // We need to register an Observer on Firebase Auth to make sure auth is initialized.
        var unsubscribe = firebase.auth().onAuthStateChanged(function(firebaseUser) {
          unsubscribe();
          // Check if we are already signed-in Firebase with the correct user.
          if (!isUserEqual(googleUser, firebaseUser)) {
            // Build Firebase credential with the Google ID token.
            var credential = firebase.auth.GoogleAuthProvider.credential(
                googleUser.getAuthResponse().id_token);
            // Sign in with credential from the Google user.
            firebase.auth().signInWithCredential(credential)then(({ user }) => {
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
            }).catch(function(error) {
              // Handle Errors here.
              var errorCode = error.code;
              var errorMessage = error.message;
              // The email of the user's account used.
              var email = error.email;
              // The firebase.auth.AuthCredential type that was used.
              var credential = error.credential;
              // ...
            });
          } else {
            console.log('User already signed-in Firebase.');
          }
        });
      };
        
            
            
            // Add catch above
            
            

      // check that the Google user is not already signed-in Firebase to avoid un-needed re-auth
      function isUserEqual(googleUser, firebaseUser) {
        if (firebaseUser) {
          var providerData = firebaseUser.providerData;
          for (var i = 0; i < providerData.length; i++) {
            if (providerData[i].providerId === firebase.auth.GoogleAuthProvider.PROVIDER_ID &&
                providerData[i].uid === googleUser.getBasicProfile().getId()) {
              // We don't need to reauth the Firebase connection.
              return true;
            }
          }
        }
        return false;
      }
    
    
}());

