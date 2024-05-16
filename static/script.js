let label = document.querySelectorAll('label').forEach(label =>{
	label.innerHTML = label.innerText.split('').map((letter, i) => `<span style="transition-delay: ${i * 50}ms">${letter}</span>`).join('');
});

let special = document.getElementById('special-char');
let minimum = document.getElementById('minimum-char');
let same = document.getElementById('same-char');
let popupBg = document.getElementById('popupBg');


function openPopupBg() {
	popupBg.classList.add("open-popupBg");
}

function closePopup(){
	special.classList.remove("open-popup");
	minimum.classList.remove("open-popup");
	same.classList.remove("open-popup");
	popupBg.classList.remove("open-popupBg");
}

function closePopupAlready(){
	let already = document.getElementById('already-user');
	let popupBgSecond = document.getElementById('popupBgSecond');

    already.style.visibility = 'hidden';
    popupBgSecond.style.visibility = 'hidden';
}

function validateForm(){
	const specialCharsRegex = /[^\w\s]/;
	let password = document.accountForm.password.value;
	let confirmPassword = document.accountForm.confirmPassword.value;

	if (password.length < 8) {
		openPopupBg();
		minimum.classList.add("open-popup");
		event.preventDefault();
	}

	if (!specialCharsRegex.test(password)) {
		openPopupBg();
		special.classList.add("open-popup");
		event.preventDefault();
	}

	if (password != confirmPassword) {
		openPopupBg();
		same.classList.add("open-popup");
		event.preventDefault();
	}

	return true;
}


function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');

    var isSidebarOpen = sidebar.style.width === '250px';

    if (!isSidebarOpen) {
        sidebar.style.width = '250px';
    } else {
        sidebar.style.width = '0';
    }
}

function closeSidebar() {
    var sidebar = document.getElementById('sidebar');
    sidebar.style.width = '0';
}

var val;
function showHide(a) {
	if (a == 0) {
		var cText = document.getElementById('show-hide-pass');
		var password = document.getElementById('password');

		if (val == 1) {
			password.type = 'password';
			cText.textContent = 'SHOW';
			val = 0;
		} else {
			cText.textContent = 'HIDE';
			password.type = 'text';
			val = 1;
		}
	} else {
		var cText = document.getElementById('show-hide-con-pass');
		var confirmPassword = document.getElementById('conpassword');

		if (val == 1) {
			confirmPassword.type = 'password';
			cText.textContent = 'SHOW';
			val = 0;
		} else {
			cText.textContent = 'HIDE';
			confirmPassword.type = 'text';
			val = 1;
		}
	}
}