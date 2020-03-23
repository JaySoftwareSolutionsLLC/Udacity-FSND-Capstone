function parseJwt (token) {
    // https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript
   var base64Url = token.split('.')[1];
   var base64 = decodeURIComponent(atob(base64Url).split('').map((c)=>{
       return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
   }).join(''));

   return JSON.parse(base64);
};

function localStoreJWTFromQueryParams() {
    let vars = [], hash;
    let hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&'); // Convert url into initial string and query params
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[i] = hash[1];
    }
    if (vars[0]) {
        let jwt = vars[0];
        // console.log(jwt);
        localStorage.setItem("jwt", jwt);
    }
}

localStoreJWTFromQueryParams();

// If token does not exist or is expired, redirect to Auth0 login page
if (!localStorage.getItem("jwt")) {
    window.location.replace("https://bjb.auth0.com/login?state=g6Fo2SBvM2RkVno0ckJtc29paUJ2bDBxVUFlTVZyTUJtMHl0cKN0aWTZIGhUekVzQjhwd0FlTUZDVkZoN0FCV2Q1YjVKYXo5T29Go2NpZNkgdEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8&client=tJQnGJ8VZ8s1QqbhcvE5bbHJ94HQQvEO&protocol=oauth2&audience=cheatsheet&response_type=token&redirect_uri=https%3A%2F%2Fflask-test-4.herokuapp.com%2Fcategories");
} else {
    let token = localStorage.getItem("jwt");
    let decodedJWT = parseJwt(token);
    // console.log(decodedJWT);
    let currentTS = Math.round((new Date()).getTime() / 1000);
    if (decodedJWT['exp'] < currentTS) {
        window.location.replace("https://bjb.auth0.com/login?state=g6Fo2SBvM2RkVno0ckJtc29paUJ2bDBxVUFlTVZyTUJtMHl0cKN0aWTZIGhUekVzQjhwd0FlTUZDVkZoN0FCV2Q1YjVKYXo5T29Go2NpZNkgdEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8&client=tJQnGJ8VZ8s1QqbhcvE5bbHJ94HQQvEO&protocol=oauth2&audience=cheatsheet&response_type=token&redirect_uri=https%3A%2F%2Fflask-test-4.herokuapp.com%2Fcategories");
    }
}



