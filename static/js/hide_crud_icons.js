let token = localStorage.getItem("jwt");

function parseJwt (token) {
    // https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript
   var base64Url = token.split('.')[1];
   var base64 = decodeURIComponent(atob(base64Url).split('').map((c)=>{
       return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
   }).join(''));

   return JSON.parse(base64);
};

let decoded_jwt = parseJwt(token);

// If the create:any permissions is not part of jwt then hide all create icons
if (decoded_jwt['permissions'].indexOf("create:any") == -1) {
    $('i.fa-plus').hide();
}
// If the update:any permissions is not part of jwt then hide all update icons
if (decoded_jwt['permissions'].indexOf("update:any") == -1) {
    $('i.fa-pencil-alt').hide();
}
// If the delete:any permissions is not part of jwt then hide all delete icons
if (decoded_jwt['permissions'].indexOf("delete:any") == -1) {
    $('i.fa-times').hide();
}