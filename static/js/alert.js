var num = 0

function alert(message, type) {
    var alertPlaceholder = document.getElementById('alertPlaceholder')
    var wrapper = document.createElement('div')
    wrapper.innerHTML = `
        <div id="alertToast${num}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `
    alertPlaceholder.append(wrapper)
    var alertToast = document.getElementById('alertToast' + num)
    var toast = new bootstrap.Toast(alertToast)
    toast.show()
    num += 1
    alertToast.addEventListener('hidden.bs.toast', function () {
        // do something...
        alertToast.parentElement.remove()
    })
    return undefined
}
