const lengthInput = document.getElementById("length");
const charCheck = document.getElementById("char");
const specialCheck = document.getElementById("special");
const passwordField = document.getElementById("password");
const button = document.getElementById("generate");
const lengthValue = document.getElementById("lengthValue");

let name_secrect = document.getElementById("name_secrect");
let password_secrect = document.getElementById("password_secrect");
let form = document.getElementById("show-form");
let form_secrect = document.getElementById("password-form");

function shuffle(str) {
  let arr = str.split("");

  for (let i = arr.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }

  return arr.join("");
}

button.addEventListener("click", function (event) {
  event.preventDefault();

  let length = parseInt(lengthInput.value);
  let letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let numbers = "0123456789";
  let special = "!@#$%&*()_+[]{}|;:<>?";
  let characters = "";
  let password = "";
  characters += numbers;
  password += numbers[Math.floor(Math.random() * numbers.length)];

  if (charCheck.checked) {
    characters += letters;
    password += letters[Math.floor(Math.random() * letters.length)];
  }

  if (specialCheck.checked) {
    characters += special;
    password += special[Math.floor(Math.random() * special.length)];
  }

  if (characters.length === 0) {
    alert("Select at least one option!");
    return;
  }

  for (let i = password.length; i < length; i++) {
    let randomIndex = Math.floor(Math.random() * characters.length);
    password += characters[randomIndex];
  }

  password = shuffle(password);

  passwordField.value = password;
});

lengthValue.textContent = lengthInput.value;

lengthInput.addEventListener("input", function () {
  lengthValue.textContent = this.value;
});

function toggles(id, toid) {
  const password = document.getElementById(id);
  const toggle = document.getElementById(toid);
  console.log(password);
  if (password.type === "password") {
    password.type = "text";
    toggle.textContent = "🙈";
  } else {
    password.type = "password";
    toggle.textContent = "👁️";
  }
}

let bool = false;

function booltoggle() {
  bool = !bool;
}

function showForm() {
  booltoggle();

  if (bool) {
    form.style.display = "block";
  }
}

function hideForm() {
  form_secrect.action = "";
  form.style.display = "none";
  bool = false;
}

function deleteSecrect(id) {
  form_secrect.action = "/delete/" + id;
  showForm();
}

function showSecrect(id) {
  let btn = document.getElementById(id);
  let element = document.getElementById("details-" + id);
  let currentDisplay = window.getComputedStyle(element).display;
  if (currentDisplay == "none") {
    form_secrect.action = "/show/" + id;
    showForm();
  } else {
    name_secrect.innerHTML = "";
    password_secrect.innerHTML = "";
    element.style.display = "none";
    btn.innerHTML = "Show";
    window.location.href = "/";
  }
}
