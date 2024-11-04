// Buttons //

// Functions //

// get student info by bedtime preference

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

// get student info by whether they use ac, fan or both

function get_student_id_by_ac_fan_preference() {

    var returned_acfan_preference_value = '';
    const acfan_preference_value = document.getElementById('acFan').value;

    if (acfan_preference_value === "acOnly") {
        console.log(acfan_preference_value);
        returned_acfan_preference_value = 'ac'
    }else if (acfan_preference_value === "fanOnly") {
        console.log(acfan_preference_value);
        returned_acfan_preference_value = 'fan'
    }else if (acfan_preference_value === "both") {
        console.log(acfan_preference_value);
        returned_acfan_preference_value = 'both'
    }else if (acfan_preference_value === "none") {
        console.log(acfan_preference_value);
        returned_acfan_preference_value = 'none'
    }

    const gender = 'F';
    console.log(acfan_preference_value);

    fetch(`http://127.0.0.1:5000/get_student_id_by_ac_fan_preference`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            gender:gender,
            ac_fan_preference: returned_acfan_preference_value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from get_student_id_by_ac_fan_preference: ', data);
    })
    .catch(error => console.error('Error: ', error));

}
