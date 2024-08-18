

// telling the settings button to do something

const settingsButtonObject = document.getElementById('settings_button_id');
settingsButtonObject.addEventListener('click', function() {

	console.log('settings button clicked');
	if (document.getElementById('settings_button_id').style.width === '10%') {
		document.getElementById('settings_button_id').style.width = '30%';
		document.getElementById('settings_button_id').style.height = '70%';
		document.getElementById('settings_button_id').innerText = "Wallpapers";

		const wallpapersDiv = document.createElement('div');
		wallpapersDiv.classList.add('wallpapersDiv_style');
		wallpapersDiv.id = 'wallpapers_div_id';
		document.getElementById('settings_button_id').appendChild(wallpapersDiv);

		const w1Button = document.createElement("button");
		w1Button.classList.add('wallpaper_buttons');  // Use 'classList' instead of 'classlist'
		w1Button.style.background = `url('C:/Users/Asus/Documents/ROOMMATE ALLOCATION APP/WALLPAPERS/w1.jpg')`;  // Correct usage of 'style.background'
		document.getElementById('wallpapers_div_id').appendChild(w1Button);

	}else{
		document.getElementById('settings_button_id').style.width = '10%';
		document.getElementById('settings_button_id').style.height = '10%';
		document.getElementById('settings_button_id').innerText = "⚙";
	};

}); 


// Telling the login button also to do something

const loginButtonObject = document.getElementById('login_button_id');
loginButtonObject.addEventListener('click', function() {

	console.log('login button clicked');
	checkUserAndPassword();
	

}); 




// Login function
function checkUserAndPassword() {
	const university_email_id = document.getElementById('university_email_id').value;
	const password = document.getElementById('password_id').value; // Capture password input

    fetch('http://127.0.0.1:5000/api/check-user-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ university_email_id: university_email_id, password: password }) // Include both university_email_id and password
    })
    .then(response => response.json())
    .then(data => {
        if (data.exists) {
            if (data.password_correct) {
                // preparing for the next screen (configs) on the same target page
                document.getElementById('result').innerText = 'Login successful!';
                
                
            } else {
                document.getElementById('result').innerText = 'Incorrect password.';
            }
        } else {
            document.getElementById('result').innerText = 'you does not exist.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    checkUserAndPassword();
});