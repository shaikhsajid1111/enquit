var match = function () {
    const text = (Math.random() + 1).toString(36).substring(7);
    const element = document.querySelector("#re-check");
    element.setAttribute('value', text);
};
var match_values = function () {
    var element = document.getElementById('re-check');
    var element2 = document.getElementById('re-check-2');
    if (element.value === element2.value) {
        document.getElementById('delete-account').classList.remove('disabled');
    }
};
