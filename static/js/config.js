const credForm = document.querySelector("#credentialModal form");
credForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    var formData = new FormData(credForm).entries()
    var response = await fetch('/api/config/credential', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(formData))
    });

    result = await response.text();
    check_response(result, response.status)
});

const profileForm = document.querySelector("#profileModal form");
profileForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    var formData = new FormData(profileForm).entries()
    var response = await fetch('/api/config/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(formData))
    });
    
    result = await response.text();
    check_response(result, response.status)
});
