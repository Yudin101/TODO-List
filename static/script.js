let label = document.querySelectorAll('label').forEach(label =>{
	label.innerHTML = label.innerText.split('').map((letter, i) => `<span style="transition-delay: ${i * 50}ms">${letter}</span>`).join('');
});

function validateForm(){
	let minimum_special = document.getElementById('minimum-special');
	let same = document.getElementById('same-char');

	const specialCharsRegex = /[^\w\s]/;
	let password = document.accountForm.password.value;
	let confirmPassword = document.accountForm.confirmPassword.value;

	if ((password.length < 8) || (!specialCharsRegex.test(password))) {
		minimum_special.classList.remove("error-msg");
		minimum_special.classList.add("error-p");
		event.preventDefault();
	}

	if (password != confirmPassword) {
		same.classList.remove("error-msg");
		same.classList.add("error-p");
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