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
    console.log(jwt);
    localStorage.setItem("jwt", jwt);
}