function updateBabyState() {
    const babyState = document.getElementById("babyState")
    fetch('/baby_details')
        .then(response => response.json())
        .then(json => babyState.innerHTML = json.baby_state)
        .catch(error => console.error(error))
}

document.addEventListener("DOMContentLoaded", function(event) {
    setInterval(updateBabyState, 1000) // interval value in milliseconds
  })