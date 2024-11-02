// Buttons //

// Functions //

function get_student_id_by_bedtime_preference() {

    const bedtime_preference_value = document.getElementById('bedtime').value;

    const gender = 'F';
    console.log(bedtime_preference_value);

    fetch(`http://127.0.0.1:5000/get_student_id_by_bedtime_preference`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            gender:gender,
            bedtime_preference: bedtime_preference_value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from get_student_id_by_bedtime_preference: ', data);
    })
    .catch(error => console.error('Error: ', error));

}