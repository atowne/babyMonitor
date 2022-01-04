function updateBabyState() {
    const babyState = document.getElementById("babyState")
    const babyTimestamps = document.getElementById('babyTimestamps')
    fetch('/baby_details')
        .then(response => response.json())
        .then(json => babyState.innerHTML = json.baby_state)
        .catch(error => console.error(error))
};

document.addEventListener("DOMContentLoaded", function(event) {
    setInterval(updateBabyState, 1000) // interval value in milliseconds
  })

async function fetchTimestamps() {
    try {
    const response = await fetch('/timestamps', {
        method: 'GET',
        credentials: 'same-origin'
    });
    const timestamps = await response.json();
    return timestamps;
    } catch (error) {
    console.error(error);
    }
}

async function updateTimestamps() {
    const babyTimestamps = document.getElementById('babyTimestamps')
    const timestamps = await fetchTimestamps();
    let timestampsArray = Object.values(timestamps)[0]

    let html = ''
    for (const timestamp of timestampsArray) {
        console.log(timestamp)
        let htmlSegment = `<tr>
                            <td>${timestamp[0]}</td>
                            <td>${timestamp[1]}</td>
                            </tr>`;

        html = htmlSegment + html; //Newest status at the top
    };

    babyTimestamps.innerHTML = html;

};

document.addEventListener("DOMContentLoaded", function(event) {
    setInterval(updateTimestamps, 10000) // interval value in milliseconds
  })

// Initialize Page
updateTimestamps()
updateBabyState()