let vars = [], hash;
let hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
for(var i = 0; i < hashes.length; i++)
{
    hash = hashes[i].split('=');
    vars.push(hash[0]);
    vars[hash[0]] = hash[1];
}
if (vars['http://localhost:5000/categories#access_token']) {
    let jwt = vars['http://localhost:5000/categories#access_token'];
    console.log(jwt);
    localStorage.setItem("jwt", jwt);
}