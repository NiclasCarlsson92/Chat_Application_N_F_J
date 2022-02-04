// // @importScripts("https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.0.0/crypto-js.min.js")
//
//
// let key;
// let encrypted_data;
//
// function generate_key() {
//     key = CryptoJS.lib.WordArray.random(16).toString();
//     document.getElementById("key").value = key;
// }
//
// function encrypt_message() {
//     let message = document.getElementById("plain").value;
//     encrypted_data = CryptoJS.AES.encrypt(message, key);
//     document.getElementById("cipher").value = encrypted_data;
// }
//
// function decrypt_message() {
//     let clearText = CryptoJS.AES.decrypt(encrypted_data, key);
//     document.getElementById("clear").value = clearText.toString(CryptoJS.enc.Utf8);
// }