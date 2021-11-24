serverUrl = window.location.origin

function getStripStatus(id) {
    fetch(`${serverUrl}/v1/strip/${id}`)
        .then(response => response.json())
        .then(data => processResponse(data))
}

function processResponse(data) {
    document.getElementById("response").innerHTML=data.name
    document.getElementById("powerswitch").checked = data.power
    document.getElementById("rgb_value").value=data.single_color_hex
    document.getElementById("brightness").value = data.single_color_brightness
}

function sendPowerRequest(element) {
    let power = document.getElementById("powerswitch").checked
    data = {
        power: document.getElementById("powerswitch").checked
    }
    id = 1;
    console.log(data);
    fetch(`${serverUrl}/v1/strip/${id}/power?power=${power}`, {
        method: 'PUT',
    })
        .then(response => response.json())
        .then(data => processResponse(data))
}

function setSingleColor(element) {
    console.log(element.dataset.strip);
    console.log(element.value);

    id = element.dataset.strip
    data = {
        single_color_hex:  document.getElementById("rgb_value").value,
        brightness: document.getElementById("brightness").value
    }

    fetch(`${serverUrl}/v1/strip/${id}/color`, {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => processResponse(data))
}